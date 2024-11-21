from django.db import models
from datetime import datetime
from uuid import uuid4

class AccountModel(models.Model):
    """Account Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=datetime.now)
    is_staff = models.BooleanField(default=False)
    class Meta:
        app_label = 'toro_auth'
        db_table = 'account'
