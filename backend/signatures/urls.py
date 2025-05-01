from django.urls import path

from . import views

urlpatterns = [
    path("", views.RegisterSignatureView.as_view(), name="register_signatures"),
    path("demo-verify/", views.DemoVerifySignatureView.as_view(), name="demo_verification"),
]
