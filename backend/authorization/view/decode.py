from functools import lru_cache

import jwt
from decouple import config
from django.http import JsonResponse
from django.urls import reverse

from helpers.types import get_logger

logger = get_logger(__name__)


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.app_id = set(config('APP_ID', cast=lambda v: [
                          s.strip() for s in v.split(',')]))
        self.public_key = self._get_public_key()
        self.exempt_urls = {reverse('login')}

    @lru_cache(maxsize=1)
    def _get_public_key(self):
        public_key_path = config('PUBLIC_KEY_PATH')
        with open(public_key_path, 'r') as key_file:
            return key_file.read()

    def _get_token_from_header(self, request):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()
        return parts[1] if len(parts) == 2 and parts[0].lower() == 'bearer' else None

    def _validate_token(self, token):
        try:
            return jwt.decode(token, self.public_key, algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            raise PermissionError('Token has expired')
        except jwt.InvalidTokenError:
            raise PermissionError('Invalid token')
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            raise PermissionError(str(e))

    def __call__(self, request):
        if request.path in self.exempt_urls:
            return self.get_response(request)

        token = self._get_token_from_header(request)
        if not token:
            return JsonResponse({'error': 'Authorization header missing or Token has expired'}, status=401)

        try:
            decoded_payload = self._validate_token(token)

            if decoded_payload.get("app_id") not in self.app_id:
                return JsonResponse({'error': 'Invalid app_id'}, status=401)

            request.token = decoded_payload
        except PermissionError as e:
            return JsonResponse({'error': str(e)}, status=401)

        return self.get_response(request)
