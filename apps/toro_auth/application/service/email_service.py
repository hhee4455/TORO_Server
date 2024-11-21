from django.core.mail import send_mail
import random
import logging
import environ
import string

# 로깅 설정
logger = logging.getLogger(__name__)

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

        env = environ.Env()
        environ.Env.read_env()  # .env 파일 읽기

        # 이메일 제목 및 내용 설정
        subject = "TORO 인증 코드 전송"
        message = f"인증번호: {verification_code}"
        from_email = env("EMAIL")

        try:
            # 이메일 발송
            send_mail(subject, message, from_email, [email])
            logger.info(f"Verification email sent successfully to {email}.")

            # 인증 코드만 반환
            return verification_code
        except Exception as e:
            # 오류가 발생하면 로그에 추가
            logger.error(f"Email sending failed for {email}: {e}")
            raise Exception(f"Email sending failed: {e}")
