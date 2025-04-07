from .views import SignatureWorkflowView
from django.urls import path

urlpatterns = [
    path("", SignatureWorkflowView.as_view(), name="list_workflow")
]
