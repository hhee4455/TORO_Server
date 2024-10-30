from dataclasses import dataclass, field
from ..types import UUID, generate_uuid, current_time
from ..utils import update_timestamp

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

    id: UUID = field(default_factory=generate_uuid)
    token: str
    created_at: datetime = field(default_factory=current_time)
    updated_at: datetime = field(default_factory=current_time)
    account_id: Optional[UUID] = None

    def refresh_token(self, new_token: str):
        """
        리프레시 토큰을 갱신하고 갱신 시간을 업데이트합니다.

        Args:
            new_token (str): 새 리프레시 토큰 값.
        """
        self.token = new_token
        self.updated_at = update_timestamp()
