from rest_framework import generics, mixins
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentDetailsSerializer, DocumentListSerializer
from .generator import generate_pdf_response


class DocumentGeneratorView(APIView):
    # TODO permission class to only allow users, not admins to visit. or for admins, use fake data.
    # TODO: windows installation is dummy stupid: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
    # write about it in readme docs and figure out CI.
    def get(self, request, id):
        # TODO: later extend this with the request body data.
        # TODO: the id should also be in body for privacy's sake?
        context = {
            "user": request.user,
        }

        return generate_pdf_response(id, context)


class DocumentListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Document.objects.filter(is_active=True)  # Only active documents
    serializer_class = DocumentListSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 

class DocumentDetailsView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Document.objects.filter(is_active=True) 
    serializer_class = DocumentDetailsSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
