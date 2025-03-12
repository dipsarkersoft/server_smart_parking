from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CreateCategory,CategoryDetail,AllCategory,UpdelCategory


router=DefaultRouter()
urlpatterns = [
  
    path('', include(router.urls)),
    path('create/', CreateCategory.as_view(),name='create'),
    path('<int:id>/', CategoryDetail.as_view(),name='details'),
    path('all/', AllCategory.as_view(),name='all_category'),

    # if req put then update else del
    path('updel/<int:id>', UpdelCategory.as_view(),name='updatedel'),
   
  
   

]