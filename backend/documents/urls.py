from django.urls import path

from . import views

urlpatterns = [
    path('<int:doc_id>/', views.DocumentGeneratorView.as_view(), name="preview_doc"),
]
