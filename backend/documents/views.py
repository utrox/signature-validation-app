from rest_framework import generics, mixins
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer
from .generator import generate_pdf_response


class DocumentGeneratorView(APIView):
    # TODO permission class to only allow users, not admins to visit. or for admins, use fake data.
    # TODO: windows installation is dummy stupid: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
    # write about it in readme docs and figure out CI.
    def get(self, request, doc_id):
        # TODO: later extend this with the request body data.
        # TODO: the doc_id should also be in body for privacy's sake.
        context = {
            "user": request.user,
        }

        return generate_pdf_response(doc_id, context)


class DocumentView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Document.objects.filter(is_active=True)  # Only active documents
    serializer_class = DocumentSerializer
    lookup_field = "id"  # Used for retrieving a single document
    
    def get(self, request, *args, **kwargs):
        # If 'id' is in the URL, retrieve a single document
        if "id" in kwargs:  
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs) 
