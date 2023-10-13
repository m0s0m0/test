from django.contrib.auth.models import User
from django.db import (
    OperationalError,
    DatabaseError,
    InternalError,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned
)

from rest_framework import status
from exceptions.service_error import ServiceException
from exceptions.error_codes import ErrorCodes


def get_user(username):
    try:
        
        user = User.objects.get(username=username)
        return user

    except ObjectDoesNotExist:
        raise ServiceException(
            status.HTTP_400_BAD_REQUEST, ErrorCodes.USER_NOT_FOUND, f'User does not exist')

    except MultipleObjectsReturned:
        raise ServiceException(
            status.HTTP_409_CONFLICT, ErrorCodes.MULTIPLE_USERS_RETURNED, f'Multiple users found')

    except (OperationalError, DatabaseError, InternalError):
        raise ServiceException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.INTERNAL_SERVER_ERROR, 'Unabe to query DB')
