from uuid import UUID, uuid4
from datetime import datetime

# 기본 ID와 시간을 생성하는 함수 정의

def generate_uuid() -> UUID:
    """
    새 고유 식별자(UUID)를 생성합니다.
    
    Returns:
        UUID: 고유 식별자 값.
    """
    return uuid4()

def current_time() -> datetime:
    """
    현재 UTC 시간을 반환합니다.
    
    Returns:
        datetime: 현재 UTC 시간.
    """
    return datetime.utcnow()
