from django.db import models
from uuid import uuid4
from ...domain.entity.social_account import SocialAccount
from .account_model import AccountModel

class SocialAccountModel(models.Model):
    """SocialAccount Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.CharField(max_length=50)
    provider_user_id = models.CharField(max_length=100)
    access_token = models.TextField()
    refresh_token = models.TextField()
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)

    def to_entity(self):
        return SocialAccount(
            id=self.id,
            provider=self.provider,
            provider_user_id=self.provider_user_id,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            account_id=self.account.id if self.account else None,
            is_verified=self.is_verified
        )

    @classmethod
    def from_entity(cls, social_account: SocialAccount):
        account_instance = AccountModel.objects.get(id=social_account.account_id) if social_account.account_id else None
        return cls(
            id=social_account.id,
            provider=social_account.provider,
            provider_user_id=social_account.provider_user_id,
            access_token=social_account.access_token,
            refresh_token=social_account.refresh_token,
            account=account_instance,
            is_verified=social_account.is_verified
        )
