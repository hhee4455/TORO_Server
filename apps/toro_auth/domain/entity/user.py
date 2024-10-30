from dataclasses import dataclass, field
from typing import Optional
from ..types import UUID, generate_uuid, current_time
from datetime import datetime

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
        last_seen (datetime): 사용자의 마지막 활동 시각.
        location (Optional[str]): 사용자의 위치.
        available_for_work (bool): 작업 가능 여부.
        follower_count (int): 팔로워 수.
        fieldwork_availability (Optional[str]): 현장 근무 가능 여부.
        field (Optional[str]): 전문 분야.
        is_active (bool): 활성화 상태 여부.
    """

    id: UUID = field(default_factory=generate_uuid)
    nickname: str
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_public: bool = False
    last_seen: datetime = field(default_factory=current_time)
    location: Optional[str] = None
    available_for_work: bool = False
    follower_count: int = 0
    fieldwork_availability: Optional[str] = None
    field: Optional[str] = None
    is_active: bool = True

    def toggle_public_status(self):
        """
        사용자의 공개 상태를 토글합니다.
        
        현재 상태가 공개면 비공개로, 비공개면 공개로 전환합니다.
        """
        self.is_public = not self.is_public
