import jwt
from django.conf import settings


def encode_jwt(user_id):
	secret = settings.JWT_SECRET

	encoded_jwt = jwt.encode({"user_info": user_id}, secret, algorithm="HS256")

	return encoded_jwt


def decode_jwt(token):
	try:
		secret = settings.JWT_SECRET

		payload = jwt.decode(token, secret, algorithms=["HS256"])
		if 'user_info' in payload:
			user_id = payload['user_info']
			return True, user_id
		return False, 0
	except Exception as e:
		return False, 0