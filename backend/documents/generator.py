from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from .models import Document


def generate_pdf_response(doc_id, context):
    document = get_object_or_404(Document, pk=doc_id)

    html_string = render_to_string(str(document.template).split("/")[-1], context)
    css_string = render_to_string("pdf.css", context)

    # Generate PDF from the rendered HTML & CSS
    pdf = HTML(string=html_string).write_pdf(stylesheets=[CSS(string=css_string)])

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=generated.pdf"
    
    return response

