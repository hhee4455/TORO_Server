from django.db import models
from datetime import datetime
from ...domain.entity.user import User
from .account_model import AccountModel
from uuid import uuid4

class UserModel(models.Model):
    """User Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nickname = models.CharField(max_length=100)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=100, blank=True, null=True)
    available_for_work = models.BooleanField(default=False)
    follower_count = models.IntegerField(default=0)
    fieldwork_availability = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='user_models', null=True)

    def to_entity(self):
        return User(
            id = self.id,
            nickname=self.nickname,
            profile_picture=self.profile_picture,
            bio=self.bio,
            is_public=self.is_public,
            last_seen=self.last_seen,
            location=self.location,
            available_for_work=self.available_for_work,
            follower_count=self.follower_count,
            fieldwork_availability=self.fieldwork_availability,
            field=self.field,
            is_active=self.is_active,
        )

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            nickname=user.nickname,
            profile_picture=user.profile_picture,
            bio=user.bio,
            is_public=user.is_public,
            last_seen=user.last_seen,
            location=user.location,
            available_for_work=user.available_for_work,
            follower_count=user.follower_count,
            fieldwork_availability=user.fieldwork_availability,
            field=user.field,
            is_active=user.is_active,
        )

    class Meta:
        app_label = 'toro_auth'
        db_table = 'user'