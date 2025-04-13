from .views import SignatureWorkflowView
from django.urls import path

urlpatterns = [
    path("", SignatureWorkflowView.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }), name="workflows"),
]
