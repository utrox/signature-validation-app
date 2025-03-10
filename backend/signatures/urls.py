from django.urls import path

from . import views

urlpatterns = [
    path("", views.RegisterSignatureView.as_view(), name="register_signature"),
]