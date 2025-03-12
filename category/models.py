from django.db import models

# Create your models here.



class CategoryModel(models.Model):
    
    name=models.CharField(max_length=30)
    price_p_h=models.IntegerField()
    total_slots=models.IntegerField()
    available_slots=models.IntegerField()
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.available_slots = self.total_slots
            super().save(*args, **kwargs)
            self.create_slots()

    def create_slots(self):
        
        for i in range(1, self.total_slots + 1):
            SlotModel.objects.create(slot_number=i, category=self)        

    def __str__(self):
        return f"{self.id}"
    

class SlotModel(models.Model):
    slot_number = models.IntegerField() 
    category = models.ForeignKey(CategoryModel, related_name="slots", on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Slot {self.slot_number} in {self.category.name}"
