# this file is added to create custom permissions.

from rest_framework.permissions import BasePermission,SAFE_METHODS

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

# this permission is to allow only author 
# of a post to update and delete said post.
class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user is obj

    