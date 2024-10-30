from dataclasses import dataclass, field
from typing import Optional
from ..types import UUID, generate_uuid

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

    id: UUID = field(default_factory=generate_uuid)
    provider: str
    provider_user_id: str
    access_token: str
    refresh_token: str
    account_id: Optional[UUID] = None

    def refresh_access_token(self, new_token: str):
        """
        접근 토큰을 갱신합니다.

        Args:
            new_token (str): 새로 갱신된 접근 토큰.
        """
        self.access_token = new_token
