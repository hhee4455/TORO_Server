from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
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
        date_joined (datetime): 계정 생성 날짜.
        is_staff (bool): 직원 여부.
        phone (Optional[str]): 사용자 전화번호.
    """
    id: UUID
    email: str
    password: str
    name: str
    date_joined: datetime = field(default_factory=datetime.now)
    is_staff: bool = False
    phone: Optional[str] = None
    verification_code: Optional[str] = None
