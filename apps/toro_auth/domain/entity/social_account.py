from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class SocialAccount:
    """
    사용자의 소셜 계정 정보를 나타내는 SocialAccount 엔티티.

    속성:
        id (UUID): 소셜 계정의 고유 식별자.
        provider (str): 소셜 계정 제공자 (예: Google, Facebook).
        provider_user_id (str): 제공자의 사용자 식별자.
        access_token (str): 소셜 계정 접근 토큰.
        refresh_token (str): 소셜 계정 갱신 토큰.
        account_id (Optional[UUID]): 연결된 계정의 ID.
    """
    id: UUID
    provider: str
    provider_user_id: str
    access_token: str
    refresh_token: str
    account_id: Optional[str] = None
