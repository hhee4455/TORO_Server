from datetime import datetime

def update_timestamp() -> datetime:
    """
    현재 UTC 시간을 반환합니다. 시간 갱신 시 사용할 수 있습니다.
    
    Returns:
        datetime: 현재 UTC 시간.
    """
    return datetime.utcnow()
