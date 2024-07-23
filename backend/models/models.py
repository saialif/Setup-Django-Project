from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


from django.contrib.auth.models import UserManager

class ActiveManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)


class TUsers(AbstractUser):
    objects = ActiveManager()
    all_objects = models.Manager()

    users_id = models.BigAutoField(
        db_column='USERS_ID', primary_key=True, editable=False)
    username = models.CharField(
        db_column='USERNAME', max_length=150, unique=True)
    email = models.EmailField(
        db_column='EMAIL', unique=True)
    is_active = models.BooleanField(
        db_column='IS_ACTIVE', default=False)
    created_at = models.DateTimeField(
        db_column='CREATED_AT', auto_now_add=True)
    created_by = models.CharField(
        db_column='CREATED_BY', max_length=150, blank=True)
    updated_at = models.DateTimeField(
        db_column='UPDATED_AT', auto_now=True)
    updated_by = models.CharField(
        db_column='UPDATED_BY', max_length=150, blank=True)
    deleted_at = models.DateTimeField(
        db_column='DELETED_AT', blank=True, null=True)
    deleted_by = models.CharField(
        db_column='DELETED_BY', max_length=150, blank=True)
    x1 = models.CharField(db_column='X1', max_length=255, blank=True)
    x2 = models.CharField(db_column='X2', max_length=255, blank=True)
    x3 = models.CharField(db_column='X3', max_length=255, blank=True)
    x4 = models.CharField(db_column='X4', max_length=255, blank=True)
    x5 = models.CharField(db_column='X5', max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'T_USERS'

    def soft_delete(self, deleted_by=None):
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.is_active = False
        self.save()

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.is_active = True
        self.save()

    def __str__(self):
        return self.username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
