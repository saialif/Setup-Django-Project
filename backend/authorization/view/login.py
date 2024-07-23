import jwt
from decouple import config
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from authorization.serializers import ValidateLoginSerializer
from helpers.response import get_response
from helpers.types import get_logger

logger = get_logger(__name__)


def get_private_key():
    private_key_path = config('PRIVATE_KEY_PATH')
    with open(private_key_path, 'r') as key_file:
        return key_file.read()


def generate_token(payload_user):
    private_key = get_private_key()
    payload = {
        "app_id": config('SELF_APP_ID'),
        "exp": timezone.now() + timezone.timedelta(hours=8),
        **payload_user
    }
    return jwt.encode(payload, private_key, algorithm='RS256')


class Login(APIView):
    def post(self, request):
        try:
            serializer = ValidateLoginSerializer(data=request.data)

            if not serializer.is_valid():
                return get_response(
                    errors=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            username = serializer.validated_data.get('username_or_email')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                user_data = {
                    "employee_name": user.username,
                    "email": user.email,
                }

                token = generate_token(user_data)

                return get_response(
                    data={"token": token},
                    status_code=status.HTTP_200_OK
                )

            return get_response(
                errors={"errors": "Invalid username or password"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Object not found: {e}")
            return get_response(
                errors={"errors": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            return get_response(
                errors={"errors": f"Database error: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return get_response(
                errors={"errors": f"An unexpected error occurred: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
