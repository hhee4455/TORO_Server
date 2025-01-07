from dataclasses import dataclass, field
from typing import Optional
from django.utils import timezone
from uuid import UUID

@dataclass
class User:
    """
    사용자의 프로필 정보와 기본 속성을 나타내는 User 엔티티.

    속성:
        id (UUID): 사용자의 고유 식별자.
        nickname (str): 사용자의 닉네임.
        profile_picture (Optional[str]): 사용자의 프로필 사진 URL.
        bio (Optional[str]): 사용자의 짧은 자기소개.
        is_public (bool): 프로필이 공개 상태인지 여부.
        last_seen (timezone): 사용자의 마지막 활동 시각.
        follower_count (int): 팔로워 수.
        is_active (bool): 활성화 상태 여부.
    """
    id: UUID
    nickname: str
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_public: bool = False
    last_seen: timezone = field(default_factory=timezone.now)
    follower_count: int = 0
    is_active: bool = True
    account_id: Optional[UUID] = None