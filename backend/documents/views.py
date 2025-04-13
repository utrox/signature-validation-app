import json

from rest_framework import generics, mixins
from rest_framework.views import APIView

from core.exceptions.exceptions import NotFoundException, BadRequestException
from signature_workflows.models import SignatureWorkflow
from .models import Document
from .serializers import DocumentDetailsSerializer, DocumentListSerializer
from .generator import generate_pdf_response


class DocumentGeneratorView(APIView):
    # TODO permission class to only allow users, not admins to visit. or for admins, use fake data.
    # TODO: windows installation is dummy stupid: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
    # write about it in readme docs and figure out CI.
    def post(self, request):
        """
        Handles the POST request to generate a document preview.
        This method generates a preview of a document based on the provided data.
        It supports two scenarios:
        1. Generating a preview before submitting the form data (using `document_id` and `form_data`).
        2. Generating a preview for an existing workflow instance (using `workflow_id`). In this case, 
            the form_data is read from the workflow instance.
        Args:
            request (Request): The HTTP request object containing the data.
                Should contain either `document_id` or `workflow_id` in the request body.
                The request body can also contain `form_data`, which is a dictionary of form fields and their values.
        Returns:
            Response: A PDF response containing the generated document preview, 
                      or an error response if the document or workflow is not found.
        """

        # If it has document_id, it means that we're generating a preview before submitting the form_data.
        # If it has workflow_id, it means that we're generating a preview for a document after it was submitted 
        # and the workflow instance exists. This can be on the admin page, or when the user wants to see the document
        # before signing it for example.
        workflow_id = request.data.get("workflow_id", None)
        document_id = request.data.get("document_id", None)
        
        if workflow_id: 
            try:
                workflow = SignatureWorkflow.objects.get(id=workflow_id)
                document_id = workflow.document.id
            except (Document.DoesNotExist, SignatureWorkflow.DoesNotExist):
                raise NotFoundException("Document not found.")
            
            context = {
                "user": workflow.user,
                "form_data": workflow.form_data,
                "preview": True
            }
        elif document_id:
            if len(Document.objects.filter(is_active=True, id=document_id)) == 0:
                raise NotFoundException("Document not found.")
            
            form_data = request.data.get("form_data", {})

            # Check for formdata validity.
            if isinstance(form_data, str):
                try:
                    form_data = json.loads(form_data)
                except json.JSONDecodeError:
                    raise BadRequestException("Invalid JSON format for form_data.")
            elif not isinstance(form_data, dict):
                raise BadRequestException("form_data must be a dictionary or JSON.")
            
            context = {
                "user": request.user,
                "form_data": form_data,
                "preview": True
            }
        else:
            raise BadRequestException("Either document_id or workflow_id is required.")
        
        return generate_pdf_response(document_id, context)
    

class DocumentListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Document.objects.filter(is_active=True)  # Only active documents
    serializer_class = DocumentListSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 


class SingleDocumentView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Document.objects.filter(is_active=True) 
    serializer_class = DocumentDetailsSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
