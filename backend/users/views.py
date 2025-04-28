import logging

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from core.exceptions import (
    UnauthorizedException,
    NotFoundException
)
from .models import UserProfile
from .serializer import UserProfileSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse(None, safe=False)

    return JsonResponse({
        "is_admin": request.user.is_staff,
        "is_signatures_recorded": len(request.user.signatures.all()) >= settings.REGISTRATION_SIGNATURES_COUNT,
    })


class UserProfileView(APIView):
    def get(self, request):
        try:
            if not request.user or not request.user.is_authenticated:
                raise UnauthorizedException("User is logged out.")
            
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            raise NotFoundException("Profile not found.")
