from rest_framework.permissions import BasePermission
from .constants import method_to_perm_keyword

class HasPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            target_object = view.target_object
        except:
            return False
        app_name = target_object["app"]
        model_name = target_object["model"]
        permission_required = f"{app_name} | {model_name} | Can {method_to_perm_keyword[request.method]} {target_object['object_type']}"
        print(permission_required)
        return request.user.has_perm(permission_required)
    
class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == int(view.kwargs['pk'])