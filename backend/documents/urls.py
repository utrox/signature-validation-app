from django.urls import path

from . import views

urlpatterns = [
    path("", views.DocumentListView.as_view(), name="list_doc"),
    path("<int:id>/", views.DocumentDetailsView.as_view(), name="single_doc"),
    path('<int:id>/preview', views.DocumentGeneratorView.as_view(), name="preview_doc"),
]
