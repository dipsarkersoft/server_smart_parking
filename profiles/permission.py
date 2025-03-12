from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsOwner(BasePermission):
    def has_permission(self, request, view):
       if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated. Please log in.")      
       return request.user.userprofile.account_type == 'Owner'
        
