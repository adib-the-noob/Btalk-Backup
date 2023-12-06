from rest_framework.permissions import BasePermission

class IsVerifiedUser(BasePermission):
    message = "User is not verified! Verify your phone number first."

    def has_permission(self, request, view):
        return request.user.verified
    