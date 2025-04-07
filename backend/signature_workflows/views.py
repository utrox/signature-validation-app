from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response

from documents.models import Document
from .models import SignatureWorkflow


class SignatureWorkflowView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = SignatureWorkflow.objects.all()
    lookup_field = "id"
    # TODO: permissions!! 
    # Only show the workflows of the user.

    """ TODO: will be used for history, workflows, etc.
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) """

    def post(self, request):
        document_id = request.data['document_id']
        form_data = request.data.get('form_data', None)

        document = get_object_or_404(Document, id=document_id)

        # Check for form data validity.
        if not form_data and document.requires_form_for_submission:
            # TODO: use raise BadRequest from exceptions.py
            return Response({"error": "Form data is required."}, status=400)
        elif form_data:
            for field in document.form.form_fields.filter(required=True):
                if field.required and field.field_id not in form_data:
                    # TODO: use raise BadRequest from exceptions.py
                    return Response({"error": f"Field '{field.label}' is required."}, status=400)

        signature_workflow = SignatureWorkflow.objects.create(
            document=document,
            user=request.user,
            form_data=form_data or {}
        )
        return Response({"id": signature_workflow.id}, status=201)
