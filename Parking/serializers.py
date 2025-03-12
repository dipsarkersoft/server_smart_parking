from rest_framework import serializers
from .models import ParkingModels
from category.serilizers import CategorySerializer
from profiles.serializers import UserProfileSerializer
from category.models import CategoryModel

class PerkingSerializer(serializers.ModelSerializer):
    user=UserProfileSerializer(read_only=True)
    category=CategoryModel()
    
      
    class Meta:
        model=ParkingModels
        fields='__all__'
        read_only_fields = ['user','ticket']