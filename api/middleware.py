import logging
import jwt
from django.http import JsonResponse

from django.utils.deprecation import MiddlewareMixin

from api.utils import decode_jwt


class AuthenticationMiddleware(MiddlewareMixin):
    # One-time configuration and initialization.

    def process_request(self, request):
        if 'authorization' in request.headers:
            token  = request.headers['authorization']
            is_valid_request, user_id = decode_jwt(token)
            if not is_valid_request:
                return JsonResponse({'message': "Authentixation Error"})
            setattr(request, 'user_id', user_id)
