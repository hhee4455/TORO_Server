from django.db import models
from src.infrastructure.toro_auth.orm.models.account_model import AccountModel

from uuid import uuid4

class RefreshTokenModel(models.Model):
    """RefreshToken Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'toro_auth'
        db_table = 'refresh_token'

    
    def __str__(self):
        return self.token