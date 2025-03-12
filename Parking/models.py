from django.db import models
from profiles.models import UserProfile
from category.models import CategoryModel,SlotModel


class ParkingModels(models.Model):
    car_name=models.CharField(max_length=40,blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE )
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    slot = models.ForeignKey(SlotModel, on_delete=models.CASCADE)
    ticket = models.CharField(max_length=60, unique=True)
    start_park = models.DateTimeField(blank=True, null=True)
    end_park = models.DateTimeField(blank=True, null=True)
    total_price = models.IntegerField(default=0)
    is_complete=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Parking {self.user.user.username}"

