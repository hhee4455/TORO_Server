# apps/toro_auth/application/service/email_service.py
from django.core.mail import send_mail
import random
import string
from apps.toro_auth.domain.entity.account import Account

class EmailService:
    """
    이메일 관련 작업을 담당하는 서비스 클래스.
    이메일 인증 코드를 생성하고, 이메일을 발송하는 기능을 제공합니다.
    """
    
    def generate_verification_code(self):
        """
        인증 코드를 생성하는 메서드.
        6자리의 숫자로 된 인증 코드를 생성합니다.
        
        Returns:
            str: 생성된 인증 코드 (6자리)
        """
        # 6자리 인증 코드 생성 (숫자만 사용)
        verification_code = ''.join(random.choices(string.digits, k=6))
        return verification_code

    def send_email(self, email):
        """
        인증 이메일을 발송하는 메서드.
        이메일로 인증 코드를 발송합니다.

        Args:
            email (str): 이메일 주소
        """
        verification_code = self.generate_verification_code()

        # 이메일 제목 및 내용 설정
        subject = "Your Email Verification Code"
        message = f"Your verification code is: {verification_code}"
        from_email = email  # 발신 이메일은 .env 파일에서 가져오는 이메일

        # 이메일 발송
        send_mail(subject, message, from_email, [email])

        # 이메일을 발송 후, 해당 이메일 계정에 인증 코드 저장
        account, created = Account.objects.get_or_create(email=email)
        account.verification_code = verification_code
        account.save()

        # 인증 코드 반환 (추후 확인용으로 사용될 수 있음)
        return verification_code
