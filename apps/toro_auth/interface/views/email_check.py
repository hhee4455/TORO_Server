# apps/toro_auth/interface/views/email_check.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.toro_auth.interface.serializers import AccountSerializer
from apps.toro_auth.application.service import EmailService
from apps.toro_auth.domain.entity import Account

class EmailRequestView(APIView):
    """
    이메일 인증 요청을 처리하는 API 뷰.
    사용자가 이메일 주소를 제공하면 해당 주소로 인증 이메일을 전송.
    """
    
    @swagger_auto_schema(
        operation_description="이메일 인증 요청 API",
        request_body=AccountSerializer,
        responses={200: 'Verification email sent.', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        """
        POST 요청을 처리하여 이메일 인증 요청을 수행한다.
        사용자가 제공한 이메일 주소로 인증 이메일을 발송한다.
        """
        # 클라이언트로부터 받은 데이터를 AccountSerializer로 직렬화 및 검증
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]  # 유효한 이메일 주소 추출

            # 이메일 발송을 처리할 서비스 객체 생성
            email_service = EmailService()
            email_service.send_email(email)  # 이메일 전송

            return Response({"message": "Verification email sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCodeView(APIView):
    """
    인증 코드 검증 요청을 처리하는 API 뷰.
    사용자가 입력한 인증 코드가 이메일로 발송된 코드와 일치하는지 확인합니다.
    """
    
    @swagger_auto_schema(
        operation_description="인증 코드 검증 API",
        request_body=AccountSerializer,
        responses={200: 'Email verified successfully.', 400: 'Invalid code.', 404: 'Account not found.'}
    )
    def post(self, request, *args, **kwargs):
        """
        POST 요청을 처리하여 이메일 인증 코드를 검증한다.
        사용자가 제공한 이메일 주소와 인증 코드가 유효한지 확인한다.
        """
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"message": "Email and code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 이메일로 해당 계정을 찾기
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"message": "Account with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # 인증 코드 확인
        if account.verification_code == code:
            # 인증 코드가 일치하면 인증 완료 처리
            account.verification_code = None  # 인증 후 코드 제거
            account.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
