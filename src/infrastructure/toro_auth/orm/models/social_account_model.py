from django.db import models
from src.infrastructure.toro_auth.orm.models.account_model import AccountModel

from uuid import uuid4

class SocialAccountModel(models.Model):
    """SocialAccount Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.CharField(max_length=50)
    provider_user_id = models.CharField(max_length=100)
    access_token = models.TextField()
    refresh_token = models.TextField()
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'toro_auth'
        db_table = 'social_account'