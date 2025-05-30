from django.conf import settings
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from authentication.permissions import IsAuthenticatedWithUserProfile, RegisteredSignatures
from core.exceptions.exceptions import BadRequestException
from .serializers import SignatureSerializer


class RegisterSignatureView(APIView):
    permission_classes = [IsAuthenticatedWithUserProfile]
    
    def post(self, request):
        serializer = SignatureSerializer(data=request.data, many=True, context={'request': request})
        
        if len(request.user.signatures.all()) >= settings.REGISTRATION_SIGNATURES_COUNT:
            raise ValidationError("You've already registered your signatures.")
        
        if len(request.data) != settings.REGISTRATION_SIGNATURES_COUNT:
            raise ValidationError(f"Exactly {settings.REGISTRATION_SIGNATURES_COUNT} signatures are required.")
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            print("Error saving signatures:", e)
            raise BadRequestException(f"Failed to save signatures. Please try again later, service might be down.")
        
        return Response(
            {"message": "Signatures registered successfully"},
            status=HTTP_201_CREATED
        )


class DemoVerifySignatureView(APIView):
    permission_classes = [
        RegisteredSignatures
    ]

    def post(self, request):
        serializer = SignatureSerializer(data=request.data, many=False, context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        # Compare with users' signatures
        errors = request.user.profile.verify_signature(serializer.model_instance())
        if errors:
            raise BadRequestException(errors)
        return Response({"message": "Signature verified!"})
