from django.db import models
from uuid import uuid4
from django.contrib.auth.hashers import make_password, check_password

class AccountModel(models.Model):
    """Account Django ORM 모델"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15) 
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'toro_auth'
        db_table = 'account'

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password: str):
        """비밀번호를 해싱하여 저장합니다."""
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password: str) -> bool:
        """안전한 비밀번호 검증을 수행합니다."""
        return check_password(raw_password, self.password)
