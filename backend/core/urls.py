"""
URL configuration for signature_validation_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, re_path, include
from .views import serve_react

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('user/', include('users.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/signatures/', include('signatures.urls')),
    path('api/workflows/', include('signature_workflows.urls')),
    re_path(
        r"^(?P<path>.*)$",
        serve_react,
        {"document_root": settings.REACT_APP_BUILD_PATH}
    )
]

# Used for serving static files in a development environment.
# In production, python manage.py collectstatic to collect static files.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
