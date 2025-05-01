from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from .models import Document


def generate_pdf(doc_id: int, context: dict) -> bytes:
    """
    Generates a PDF from the given document's stored template and context.
    Args:
        doc_id (int): The ID of the document to generate the PDF from.
        context (dict): The context data to render the PDF with.
    Returns:
        bytes: The generated PDF as bytes.
    """
    document = get_object_or_404(Document, pk=doc_id)

    html_string = render_to_string(str(document.template).split("/")[-1], context)
    css_string = render_to_string("pdf.css", context)

    # Generate PDF from the rendered HTML & CSS
    pdf = HTML(string=html_string).write_pdf(stylesheets=[CSS(string=css_string)])
    return pdf


def generate_pdf_response(doc_id: int, context: dict) -> HttpResponse:
    """
    Generates a PDF response for the generated using the given document's template and the context.
    Args:
        doc_id (int): The ID of the document to generate the PDF from.
        context (dict): The context data to render the PDF with.
    Returns:
        HttpResponse: The HTTP response containing the generated PDF.
    """
    pdf = generate_pdf(doc_id, context)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=generated.pdf"
    
    return response
