from django.db import models
from datetime import datetime
from ...domain.entity.refresh_token import RefreshToken
from .account_model import AccountModel
from uuid import uuid4

class RefreshTokenModel(models.Model):
    """RefreshToken Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)

    def to_entity(self):
        return RefreshToken(
            id=self.id,
            token=self.token,
            created_at=self.created_at,
            updated_at=self.updated_at,
            account_id=self.account.id if self.account else None,
        )

    @classmethod
    def from_entity(cls, refresh_token: RefreshToken):
        account_instance = AccountModel.objects.get(id=refresh_token.account_id) if refresh_token.account_id else None
        return cls(
            id=refresh_token.id,
            token=refresh_token.token,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
            account=account_instance,
        )
    class Meta:
        app_label = 'toro_auth'