from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerkingSerializer
from .models import ParkingModels
from profiles.permission import IsOwner
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from category.models import CategoryModel,SlotModel
import uuid
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import os
import environ
from django.db.models import Sum
from category.serilizers import CategorySerializer
from django.db.models import F


env=environ.Env()
environ.Env.read_env()




B_URL="https://backend-parking-p4dd.onrender.com/parking/"
F_URL="https://front-parking.vercel.app/"

# B_URL= "http://127.0.0.1:8000/parking/"
# F_URL="http://localhost:5173/"


S_ID=env('STORE_ID')
S_PASS=env('STORE_PASS')




def generate_id():
    return str(uuid.uuid4())




class CreateParkings(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=PerkingSerializer(data=request.data)
        if serializer.is_valid():
             name = serializer.validated_data['car_name']
             categ = serializer.validated_data['category']
             slot = serializer.validated_data['slot']
             start_date=serializer.validated_data['start_park']
             end_date=serializer.validated_data['end_park']
            
                
            
             if not start_date or not end_date:
                 return Response({"error": "Start date And End date must be Needed"})                                                                 
             if start_date < now():
                
                return Response({"error": "Start date must be in the future"})
             if end_date <= start_date:
                return Response({"error": "End date must be after Start date"})
             
             if categ:
                isctg=CategoryModel.objects.get(id=categ.id)
               
                
                isExist=ParkingModels.objects.filter(
                    category=categ, slot=slot,
                    start_park__lt=end_date, 
                    end_park__gt=start_date   
                        )
                if isExist.exists():
                        return Response({
                            "error": "Slot is already booked for the selected dates"})                                       
                
                total_time=end_date-start_date                  
                total__hours = total_time.total_seconds() / 3600
                    

                priceper_h=isctg.price_p_h

                if total__hours <=1:
                        total__hours=1


                total_price=total__hours*priceper_h  


                parking = ParkingModels.objects.create(
                            user=request.user.userprofile,
                            ticket=generate_id(),                           
                            slot=slot,
                            car_name=name,
                            category=categ,
                            start_park=start_date,
                            end_park=end_date,
                            total_price=total_price
                            )
                
                
                isctg.available_slots -= 1               
                isctg.save()

                res = PerkingSerializer(parking)
                return Response( {
                                    "message": "Parking created successfully !",
                                    "data": res.data,
                                    'status':201,
                                    }
                                )
                 
                    
                 
        return Response(serializer.errors)


class AvailableSlotView(APIView):

    # permission_classes=[IsAuthenticated]

    def get(self,request):
        cat_id =request.query_params.get('category_id')      
        start_time =request.query_params.get('start_time')      
        end_time =request.query_params.get('end_time')

        if not cat_id or not start_time or not end_time:
            return Response(
                {"error": "Category, start_time, and end_time are required!"}
                 )
        ctg = CategoryModel.objects.get(id=cat_id)
        all_slot=SlotModel.objects.filter(category=ctg)
        availableSlot=[]

        for slot in all_slot:
            is_book=ParkingModels.objects.filter(
                category=ctg,
                slot=slot,
                start_park__lt=end_time,
                end_park__gt=start_time
            ).exists()
            if not is_book:
                availableSlot.append({

                     "id": slot.id, "slot_number": slot.slot_number

                    })

        return Response({
            "message": "All Free Slots ",
            "data": availableSlot
        })        

       

class CheakTotal(APIView):
     permission_classes=[IsAuthenticated]

     def put(self,request,id):
          
          isparking=ParkingModels.objects.get(id=id)
          

          if isparking:      
                      
               ticket=request.data.get('ticket')
               if isparking.ticket!=ticket:
                    return Response({
                    'message':"Wrong Ticket Please Cheak"
                    
                                })
               
               total_price=isparking.total_price      
               
               return Response({
                    'total_price':round(total_price),
                    'trans_ticket':generate_id(),
                    'parking_id':isparking.id,
                    'message':"Your Total Bill"
               }) 

                    
          else:
               return Response({
                    'message':"ID Wrong Please Cheak"
               })          
                             
                
class BackCar(APIView):
      permission_classes=[IsAuthenticated]

      def put(self,request,id):
                      
          isparking=ParkingModels.objects.get(id=id)
        
          if isparking:
               catewise=CategoryModel.objects.get(id=isparking.category.id)
               catewise.available_slots+=1            
               isparking.is_complete=True
               catewise.save()
               isparking.save()
               return Response({
                        'messages':"Thanks For Parking",
                        'status':"Sucess"
                    })



class AllParkings(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        data = ParkingModels.objects.all().order_by('-start_park')
        
        if self.request.user.userprofile.account_type =='User':
             res= data.filter(user=self.request.user.userprofile)
             serializer=PerkingSerializer(res,many=True)
             for item in serializer.data:
                item.pop("ticket", None)         
         
             return Response(
                {
                    'data':serializer.data,
                    'messages':'Your All Parkings'
                }
             )
        else:
            serializer=PerkingSerializer(data,many=True)
           
            for item in serializer.data:
                item.pop("ticket", None)
          
        
            
            return Response(
                {
                    'data':serializer.data,
                    'messages':' All Parkings'
                }
                )
        


class PaymentView(APIView):

    def post(self,request):

        res=request.data
        trans_id=generate_id()
    

        settings = { 'store_id': S_ID, 'store_pass': S_PASS, 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = res['totalammount']
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trans_id
        post_body['success_url']=f"{B_URL}payment/success/{trans_id}/"
        post_body['fail_url'] =f"{B_URL}payment/failed/" 
        post_body['cancel_url'] =f"{B_URL}payment/failed/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] =request.user.userprofile.mobile_no,
        post_body['cus_add1'] = "Dhaka"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcz.createSession(post_body) 
        
        return Response({
            "message":"payment sucess",
            "data":response,
            'transId':trans_id
                     }) 



@csrf_exempt
async def paymentSucess(request, trans_id: str):
    return redirect(f'{F_URL}payment/sucess/{trans_id}')
    


@csrf_exempt
async def paymentfailed(request):
    return redirect(f'{F_URL}payment/failed')      
     

   


    

