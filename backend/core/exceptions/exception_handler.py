import logging
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler

from .exceptions import CustomException


logger = logging.getLogger(__name__)

# TODO: edit exception handler to make it compatible with rest framework
class CustomExceptionHandlerMiddleware:
    """
    Custom exception handler middleware, so that all exceptions are handled
    uniformly and similarly to graphQL errors.
    Also, added logging for the exceptions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def _process_custom_exception(self, exception):
        if isinstance(exception.message, str):
            exception.message = [exception.message]

        return {
            "errors": [
                {
                    "message": error
                } for error in exception.message
            ],
        }

    def _process_default_exception(self, exception):
        if isinstance(exception, JSONDecodeError):
            exception.status_code = 400

        if isinstance(exception, ValidationError):
            exception.status_code = 400

        return {
            "errors": [
                {
                    "message": str(exception)
                }
            ],
        }

    def process_exception(self, _, exception):
        # Match the response format to the default graphQL error,
        # so that it's easier to handle on the frontend.
        logger.error(exception, exc_info=True)
        if isinstance(exception, CustomException):
            response_data = self._process_custom_exception(exception)
        else:
            response_data = self._process_default_exception(exception)

        status_code = getattr(exception, 'status_code', 500)

        return JsonResponse(response_data, status=status_code)
