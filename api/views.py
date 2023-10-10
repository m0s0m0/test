import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.core.exceptions import (
    ObjectDoesNotExist, 
    MultipleObjectsReturned
    )

from .utils import encode_jwt
from .serializers import LoginSerializer





class ProfileView(APIView):
    """
    View to list profile of user.

    * Requires token authentication.
    
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        username = request.user_id
        user = User.objects.get(username=username)

        return Response({'first_name': user.username})


class LoginView(APIView):
    """
    VIew for login of user

    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        return valid user with jwt
        """

        response_dict = {
            'data': [],
            'success': False,
            'error_message': ''
        }
        try:
            data = request.data
            logging.error(f'data{data}')
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                response_dict['error_message'] = 'Not Valid request data'
                return Response(response_dict)

            username = data['username']
            password = data['password']

            logging.error(f'data{username}password{password}')
            user = authenticate(username=username, password=password)
            if user is None:
                response_dict['error_message'] = 'Invalid username or passwrod'
                return Response(response_dict)        

            jwt = encode_jwt(user.username)
            response_dict['data'] = dict(first_name=user.first_name, token=jwt)
            response_dict['success'] = True

            return Response(response_dict)

        except Exception as e:
            return response_dict        

            

        



