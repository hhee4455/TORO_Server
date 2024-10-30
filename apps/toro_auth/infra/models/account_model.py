from django.db import models
from uuid import uuid4
from datetime import datetime
from ...domain.entity.account import Account

class AccountModel(models.Model):
    """Account Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=datetime.utcnow)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def to_entity(self):
        return Account(
            id=self.id,
            email=self.email,
            password=self.password,
            name=self.name,
            date_joined=self.date_joined,
            is_staff=self.is_staff,
            phone=self.phone,
            is_verified=self.is_verified
        )

    @classmethod
    def from_entity(cls, account: Account):
        return cls(
            id=account.id,
            email=account.email,
            password=account.password,
            name=account.name,
            date_joined=account.date_joined,
            is_staff=account.is_staff,
            phone=account.phone,
            is_verified=account.is_verified
        )
