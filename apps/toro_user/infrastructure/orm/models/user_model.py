from django.db import models
from apps.toro_auth.infrastructure.orm.models.account_model import AccountModel
from uuid import uuid4

class UserModel(models.Model):
    """User Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nickname = models.CharField(max_length=100)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now_add=True)
    follower_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'toro_user'
        db_table = 'user'