from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):

    #(override)
    def has_object_permission(self, request, view, obj):
        print('obj.owner',obj.owner)
        print('request.user',request.user)
        return obj.owner == request.user
        