from rest_framework import permissions

class IsOwnerTrucks(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# For objects that belong to trucks
class IsOwnerTruckObjects(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.truck.owner == request.user

# For ratings, ensures that the user is the only one that can change
class IsOwnerRatings(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
