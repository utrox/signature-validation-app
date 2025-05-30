import json
import logging

from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

from core.exceptions import (
    BadRequestException,
    UnauthorizedException,
    ConflictException,
)
from .validators import validate_password, validate_email

User = get_user_model()
logger = logging.getLogger(__name__)


@require_POST
def login_view(request):
    if not request.body:
        raise BadRequestException("Request body is empty.")

    json_data = json.loads(request.body)
    username = json_data.get('username', '')
    password = json_data.get('password', '')
    if not username or not password:
        raise BadRequestException("Username and password are required.")

    user = authenticate(username=username, password=password)
    if user is not None:
        logging.info("User %s authenticated successfully.", user.username)
        login(request, user)
        return HttpResponse(status=204)

    raise UnauthorizedException("Invalid username or password.")


@require_POST
def logout_view(request):
    logout(request)
    logger.info("User %s logged out.", request.user.id)
    return HttpResponse(status=204)


@require_POST
def register_view(request):
    if not request.body:
        raise BadRequestException("Request body is empty.")

    json_data = json.loads(request.body)
    email = json_data.get('email', '')
    username = json_data.get('username', '')
    password = json_data.get('password', '')

    if not email or not username or not password:
        raise BadRequestException("Username, email and password are required.")

    errors = validate_password(password)

    if errors:
        raise BadRequestException(errors)
    
    validate_email(email)

    try:
        User.objects.create_user(
            email=email,
            username=username, 
            password=password
        )
        
        logger.info("User %s successfully created.", username)
    except IntegrityError as exc:
        raise ConflictException("Username already exists.") from exc

    return HttpResponse(status=201)
