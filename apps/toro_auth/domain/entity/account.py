from dataclasses import dataclass, field
from typing import Optional
from django.utils import timezone
from uuid import UUID

@dataclass
class Account:
    """
    사용자의 계정 정보를 나타내는 Account 엔티티.

    속성:
        id (UUID): 계정의 고유 식별자.
        email (str): 계정 이메일 주소.
        password (str): 계정 비밀번호.
        name (str): 사용자 이름.
        date_joined (timezone): 계정 생성 날짜.
        is_staff (bool): 직원 여부.
    """
    id: UUID
    email: str
    password: str
    name: str
    date_joined: timezone = field(default_factory=timezone.now)
    is_staff: bool = False
