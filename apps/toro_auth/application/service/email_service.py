from django.core.mail import send_mail
import random
import logging
import environ
import string
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta

from apps.toro_auth.application.repositories.account_repository import AccountRepository

verification_codes = {}
# 로깅 설정
logger = logging.getLogger(__name__)

class EmailService:
    """
    이메일 관련 작업을 담당하는 서비스 클래스.
    """

    def __init__(self, account_repository : AccountRepository):
        """
        레포지토리 인스턴스를 초기화합니다.
        """
        self.account_repository = account_repository

    def generate_verification_code(self):
        """
        인증 코드를 생성하는 메서드.
        """
        # 6자리 인증 코드 생성 (숫자만 사용)
        verification_code = ''.join(random.choices(string.digits, k=6))
        return verification_code

    def send_email(self, email):
        """
        중복된 이메일이 없을 때 인증 이메일을 발송하는 메서드.
        """

        # 이메일 중복 확인
        if self.account_repository.find_by_email(email) is not None:
            raise ValidationError("이미 등록된 이메일입니다.")

        verification_code = self.generate_verification_code()

        # 이메일 제목 및 내용 설정
        subject = "TORO email verification"
        message = f"인증번호: {verification_code}"
        from_email = "hhee445567@gmail.com"

        try:
            # 이메일 발송
            send_mail(subject, message, from_email, [email])
            logger.info(f"Verification email sent successfully to {email}.")

            expiration_time = timezone.now() + timedelta(minutes=10)
            verification_codes[email] = {'code': verification_code, 'expires_at': expiration_time}

            # 인증 코드만 반환
            return verification_code
        except Exception as e:
            # 오류가 발생하면 로그에 추가
            logger.error(f"Email sending failed for {email}: {e}")
            raise Exception(f"Email sending failed: {e}")

    def verify_code(self, email, code):
        """
        이메일과 인증번호를 비교하여 유효성 검사를 합니다.
        """
        stored_data = verification_codes.get(email)

        if stored_data:
            if stored_data['code'] == code and stored_data['expires_at'] > timezone.now():
                del verification_codes[email]  # 인증 성공 시 메모리에서 삭제
                return True
        return False
