from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrerSerializer,LoginSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from django.contrib.auth.models import User
# Create your views here.

class UserRegisterView(APIView):
    serializer_class=RegistrerSerializer
    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            resp=serializer.data
            resp.pop('password', None) 
            resp.pop('confirm_password', None) 
            resp.pop('account_type', None) 
                                                     
            return Response ({
                'status':201,
                'message':"Thanks For create Account",
                'data':resp
            })
        return Response({
            'error':serializer.errors
        })
    

class UserLoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']

            user=authenticate(username=username,password=password)

            if user:
                token,_=Token.objects.get_or_create(user=user)
                login(request,user)
                return Response(
                    {
                    'token':token.key,
                    'user_id':user.id,
                    'account_type':user.userprofile.account_type
                   
                })
            else:

                return Response({
                    'error':'Invalid Credintial'
                })
        return Response(serializer.errors) 


class UserByIDView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self,request, user_id):
    
        try:
            
            user_profile = UserProfile.objects.get(user_id=user_id)
            
            user = {
                'id': user_profile.user.id,
                'first_name': user_profile.user.first_name,
                'last_name': user_profile.user.last_name,
                'email': user_profile.user.email,
                'account_type': user_profile.account_type,
                'mobile_no': user_profile.mobile_no,
                
            }
            
            return Response({

                'status': 'success',
                'data': user

                })
    
        except UserProfile.DoesNotExist:
        
            return Response(
                {
            'status': 'error',
            'message': 'User profile not found'
              } 
              )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    

class UserUpdateView(APIView):
  
    permission_classes = [IsAuthenticated]
     
    
    def put(self,request):
        user=request.user
        qu_user=User.objects.get(id=user.id)
        
        email=request.data.get('email',qu_user.email)
        first_name=request.data.get('first_name',qu_user.first_name)
        last_name=request.data.get('last_name',qu_user.last_name)
        mobile_no=request.data.get('mobile_no',qu_user.userprofile.mobile_no)
       
        #print(email,address,mobile_no,last_name,first_name)

        
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.userprofile.mobile_no=mobile_no
        
        user.save()
        user.userprofile.save()
        
        return Response({
            "message": "User updated successfully.",
            "status":201,
             'data':{
                    "id":user.id,
                   "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mobile_no": user.userprofile.mobile_no,
                    "account_type":user.userprofile.account_type,

                    
             }
            
            })