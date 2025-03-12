from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AllParkings,CreateParkings,CheakTotal,BackCar,PaymentView,paymentSucess,paymentfailed,AvailableSlotView


router=DefaultRouter()
urlpatterns = [
  
    path('', include(router.urls)),
    path('all/', AllParkings.as_view(),name='all_parkings'),
    
    path('availableSlot/', AvailableSlotView.as_view(),name='availableSlot'),

    path('create/', CreateParkings.as_view(),name='create_parkings'),
    path('cheaktotal/<int:id>', CheakTotal.as_view(),name='cheaktotal'),
    path('back/<int:id>', BackCar.as_view(),name='backcar'),
    path('payment/',PaymentView.as_view(), name='Payment_view'),
    path('payment/success/<str:trans_id>/', paymentSucess,name='Payment_red'),
    path('payment/failed/', paymentfailed,name='Payment_failed'),
]