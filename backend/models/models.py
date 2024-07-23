from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone


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

    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    date_joined = models.DateTimeField()
    users_id = models.BigAutoField(db_column='USERS_ID', primary_key=True)
    username = models.CharField(
        db_column='USERNAME', unique=True, max_length=150)
    email = models.CharField(db_column='EMAIL', unique=True, max_length=254)
    is_active = models.BooleanField(db_column='IS_ACTIVE')
    created_at = models.DateTimeField(db_column='CREATED_AT')
    created_by = models.CharField(
        db_column='CREATED_BY', max_length=150, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='UPDATED_AT')
    updated_by = models.CharField(
        db_column='UPDATED_BY', max_length=150, blank=True, null=True)
    deleted_at = models.DateTimeField(
        db_column='DELETED_AT', blank=True, null=True)
    deleted_by = models.CharField(
        db_column='DELETED_BY', max_length=150, blank=True, null=True)
    x1 = models.CharField(db_column='X1', max_length=255,
                          blank=True, null=True)
    x2 = models.CharField(db_column='X2', max_length=255,
                          blank=True, null=True)
    x3 = models.CharField(db_column='X3', max_length=255,
                          blank=True, null=True)
    x4 = models.CharField(db_column='X4', max_length=255,
                          blank=True, null=True)
    x5 = models.CharField(db_column='X5', max_length=255,
                          blank=True, null=True)

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
