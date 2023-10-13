import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.utils.decorators import method_decorator


from exceptions.service_error import ServiceException
from exceptions.error_codes import ErrorCodes

from utils.response import SendResponse

from .utils import encode_jwt
from .serializers import LoginSerializer
from .queries import get_user





class ProfileView(APIView):
    """
    View to list profile of user.

    * Requires token authentication.
    
    """
    @method_decorator(cache_page(60 * 15))
    def get(self, request, format=None):
        """
        Return profile of the user with the help of token.
        """
        try:

            username = request.user_id
            user = get_user(username)
            response_dict = dict(first_name=user.username)
            return SendResponse(
                status.HTTP_200_OK, response_dict, message='Fetched analysis successfully')

        except AttributeError:
            return SendResponse(
                status.HTTP_401_UNAUTHORIZED, None, ErrorCodes.INVALID_AUTHENTICATION.value, 
                'Invalid authentication')

        except ServiceException as e:
            return SendResponse(e.status_code, None, 
                error_code=e.error_code, message=e.message)

        except Exception as e:
            logging.error(f'error while fetching  profile {e.message} of user')
            return SendResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, None,
                error_code=500, message=str(e))



class LoginView(APIView):
    """
    VIew for login of user

    """
    def post(self, request, format=None):
        """
        return valid user with jwt
        """

        response_dict = dict()
        try:
            data = request.data
            logging.error(f'data{data}')
            serializer = LoginSerializer(data=data)
            
            if not serializer.is_valid():
                raise ServiceException(status.HTTP_400_BAD_REQUEST, 
                    ErrorCodes.REQUEST_VALIDATION_FAILED, 'Invalid post data')

            username = data['username']
            password = data['password']
            
            user = get_user(username)
            
            user = authenticate(username=username, password=password)
            if user is None:
                response_dict['error_message'] = 'Invalid username or passwrod'
                raise ServiceException(status.HTTP_401_UNAUTHORIZED,
                               ErrorCodes.INVALID_AUTHENTICATION, 'Invalid Credentials')

            jwt = encode_jwt(user.username)
            response_dict = dict(first_name=user.first_name, token=jwt)
            
            return SendResponse(
                status.HTTP_200_OK, response_dict, message='Fetched analysis successfully')

        except ServiceException as e:
            return SendResponse(e.status_code, None, 
                error_code=e.error_code, message=e.message)

        except Exception as e:
            logging.error(f'error while login {e.message} with Credentials {username}, {password}')
            return SendResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, None,
                error_code=500, message=str(e))


