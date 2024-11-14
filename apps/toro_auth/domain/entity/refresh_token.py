from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class RefreshToken:
    """
    계정의 리프레시 토큰 정보를 나타내는 RefreshToken 엔티티.

    속성:
        id (UUID): 리프레시 토큰의 고유 식별자.
        token (str): 리프레시 토큰 값.
        created_at (datetime): 토큰 생성 시각.
        updated_at (datetime): 마지막 갱신 시각.
        account_id (Optional[UUID]): 연결된 계정의 ID.
    """
    id: UUID
    token: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    account_id: Optional[str] = None


