
from rest_framework.views import APIView
from .template_utils import TemplateUtils
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
            "utils": TemplateUtils()  
        }

        return generate_pdf_response(doc_id, context)
