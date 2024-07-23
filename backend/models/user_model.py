from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


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
        db_column='CREATED_BY', max_length=150, blank=True, null=True)
    updated_at = models.DateTimeField(
        db_column='UPDATED_AT', auto_now=True)
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
        managed = False
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
