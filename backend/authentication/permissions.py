from rest_framework.permissions import BasePermission
from django.conf import settings


class IsAuthenticatedWithUserProfile(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile
    

class RegisteredSignatures(BasePermission):
    """
    Allows access only to authenticated users who've recorded signatures.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.signatures.count() >= settings.REGISTRATION_SIGNATURES_COUNT
