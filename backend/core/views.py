import logging
import posixpath
from pathlib import Path

from django.http import HttpResponse
from django.utils._os import safe_join
from django.views.static import serve as static_serve
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def serve_react(request, path, document_root=None):
    logging.info("Serving static file: %s", path)
    path = posixpath.normpath(path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))

    # If the file exists, then serve the it, because
    # the user is requesting a static file.
    if fullpath.is_file():
        return static_serve(request, path, document_root)

    # Serve index.html for all other paths, because
    # the user is requesting a frontend route. Let React
    # handle the routing, and possible 404.
    return static_serve(request, "index.html", document_root)


def serve_media_images(request, path, document_root=None):
    logging.info("Serving media file: %s", path)
    if request.user.is_authenticated:
        path = posixpath.normpath(path).lstrip("/")
        return static_serve(request, path, document_root)

    logging.error("User is not authenticated.")
    return HttpResponse(status=403)
