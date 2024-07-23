from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(
                Q(email=username) | Q(username=username))
        except user_model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
""" from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        start_time = datetime.now()
        user_model = get_user_model()

        try:
            user_query_start_time = datetime.now()
            user = user_model.objects.get(
                Q(email=username) | Q(username=username)
            )
            user_query_end_time = datetime.now()
            logger.debug(
                f"User query time: {user_query_end_time - user_query_start_time}")
        except user_model.DoesNotExist:
            user_not_found_time = datetime.now()
            logger.debug(
                f"User not found time: {user_not_found_time - start_time}")
            return None

        password_check_start_time = datetime.now()
        if user.check_password(password):
            password_check_end_time = datetime.now()
            logger.debug(
                f"Password check time: {password_check_end_time - password_check_start_time}")
            return user
        password_check_end_time = datetime.now()
        logger.debug(
            f"Password check failed time: {password_check_end_time - password_check_start_time}")

        end_time = datetime.now()
        logger.debug(
            f"Total authentication process time: {end_time - start_time}")

        return None """
