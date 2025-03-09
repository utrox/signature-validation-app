from django.urls import path

from . import views

urlpatterns = [
    path("", views.DocumentView.as_view(), name="list_doc"),
    path("<int:doc_id>/", views.DocumentView.as_view(), name="single_doc"),
    path('<int:doc_id>/preview', views.DocumentGeneratorView.as_view(), name="preview_doc"),
]
