from django.conf import settings
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .serializers import SignatureSerializer


class RegisterSignatureView(APIView):
    # TODO: permission group -> users
    def post(self, request):
        serializer = SignatureSerializer(data=request.data, many=True, context={'request': request})
        
        # TODO: Permission class instead?
        if len(request.user.signatures.all()) >= settings.REGISTRATION_SIGNATURES_COUNT:
            raise ValidationError("You've already registered your signatures.")
        
        if len(request.data) != settings.REGISTRATION_SIGNATURES_COUNT:
            raise ValidationError(f"Exactly {settings.REGISTRATION_SIGNATURES_COUNT} signatures are required.")
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response(
            {"message": "Signatures registered successfully"},
            status=HTTP_201_CREATED
        )


class DemoVerifySignatureView(APIView):
    # TODO: permission:
    #   - only non-staff users
    #   - only users that have uploaded signatures
    def post(self, request):
        serializer = SignatureSerializer(data=request.data, many=False, context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        # Compare with users' signatures
        errors = request.user.profile.verify_signature(serializer.model_instance())
        if errors:
            return Response(errors, status=400)
        return Response({"message": "Signature verified!"})
