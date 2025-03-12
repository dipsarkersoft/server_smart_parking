from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('profiles.urls')),
    path('category/',include('category.urls')),
    path('parking/',include('Parking.urls')),
   

]