from rest_framework.permissions import BasePermission,SAFE_METHODS

# Super user 
class IsSuperUser(BasePermission):
    def has_permission(self,request):
        if request.user.is_superuser:
            return True
        return False

class IsStaff(BasePermission):
    def has_permission(self,request):
        if request.user.is_staff:
            return True
        return False

class IsStaffReadOnly(BasePermission):
    def has_permission(self,request):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True
        return False

