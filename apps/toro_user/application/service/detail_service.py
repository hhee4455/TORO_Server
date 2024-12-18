from apps.toro_user.application.repositories.detail_repository import DetailRepository


class DetailService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    """

    def __init__(self, user_repository: DetailRepository):
        self.user_repository = user_repository


