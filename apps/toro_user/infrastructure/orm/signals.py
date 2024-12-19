from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.toro_auth.infrastructure.orm.models.account_model import AccountModel
from apps.toro_user.infrastructure.orm.models.user_model import UserModel

DEFAULT_PROFILE_PICTURE = "https://toro-backend.s3.ap-northeast-2.amazonaws.com/profile/profile.png"

@receiver(post_save, sender=AccountModel)
def create_user_for_account(sender, instance, created, **kwargs):
    """
    AccountModel이 생성되면 UserModel에 데이터를 자동으로 추가합니다.
    """
    if created:  # Account가 새로 생성된 경우만 실행
        UserModel.objects.create(
            account=instance,
            nickname=instance.name,  # Account의 name을 nickname으로 사용
            is_active=True,
            profile_picture=DEFAULT_PROFILE_PICTURE,  # 기본 프로필 이미지 설정
        )
