from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from profiles.permission import IsOwner
from .serilizers import CategorySerializer
from .models import CategoryModel
# Create your views here.


class CreateCategory(APIView):

    permission_classes=[IsOwner]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    


class CategoryDetail(APIView):

    def get(self, request, id):
        try:

            category = CategoryModel.objects.get(id=id)

            serializer = CategorySerializer(category)
            
            return Response(serializer.data)
        
        except CategoryModel.DoesNotExist:
          
            return Response({"error": "Category not found."})




class AllCategory(APIView):

    def get(self, request):
        data = CategoryModel.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)
    



class UpdelCategory(APIView):
    permission_classes=[IsOwner]


    def put(self, request,id):
        
        try:
            category = CategoryModel.objects.get(id=id)

        except CategoryModel.DoesNotExist:
            return Response({'error': 'Categories not found'})

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

    def delete(self,request,id):
        
        try:
             category = CategoryModel.objects.get(id=id)
        except CategoryModel.DoesNotExist:

            return Response({'error': 'Categories not found'})       
        category.delete()
        return Response({'message': 'Categories deleted successfully'})
