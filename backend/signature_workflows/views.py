from rest_framework.response import Response
from rest_framework import viewsets

from .models import SignatureWorkflow
from .serializer import (
    SignatureWorkflowListSerializer, 
    SignatureWorkflowCreateSerializer,
    SignatureVerificationSerializer,
    SignatureWorkflowCancelSerializer
    )


class SignatureWorkflowView(viewsets.ModelViewSet):
    lookup_field = "id"
    # TODO: permissions!! 
    def get_queryset(self):
        return SignatureWorkflow.objects.filter(user=self.request.user).order_by("-created_at")
    
    def get_serializer_class(self):
        MAPPING = {
            "list": SignatureWorkflowListSerializer,
            "create": SignatureWorkflowCreateSerializer,
            "update": SignatureVerificationSerializer,
            "destroy": SignatureWorkflowCancelSerializer
        }
        return MAPPING.get(self.action, SignatureWorkflowListSerializer)
    
    def get_serializer(self, *args, **kwargs):
        return self.get_serializer_class()(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        workflow = serializer.save()
        return Response({"id": workflow.id}, status=201)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Signature verified!"})
    
    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)
