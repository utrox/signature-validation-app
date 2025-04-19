from django.urls import path
from . import views


urlpatterns = [
    path('me/', views.me_view, name="me_view"),
    path('profile/', views.UserProfileView.as_view(), name="user_profile_view"),
]
