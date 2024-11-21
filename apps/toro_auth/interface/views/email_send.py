import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.toro_auth.interface.serializers import EmailRequestSerializer, EmailResponseSerializer
from apps.toro_auth.application.service.email_service import EmailService
from rest_framework.permissions import AllowAny
import smtplib

# 로거 설정
logger = logging.getLogger(__name__)

class EmailRequestView(APIView):
    permission_classes = [AllowAny]

    """
    이메일 인증 요청을 처리하는 API 뷰.
    사용자가 이메일 주소를 제공하면 해당 주소로 인증 이메일을 전송.
    """
    @swagger_auto_schema(
        operation_description="이메일 인증 요청 API",
        request_body=EmailRequestSerializer,
        responses={200: EmailResponseSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = EmailRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            logger.info(f"Received email: {email}")

            email_service = EmailService()
            try:
                # 이메일 전송 시도
                email_service.send_email(email)

                # 성공 응답 데이터
                response_data = {"success": 1, "message": "이메일이 성공적으로 전송 되었습니다."}
                response_serializer = EmailResponseSerializer(data=response_data)

                # 응답 직렬화가 유효한지 확인
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except smtplib.SMTPException as e:
                # SMTP 관련 오류 로깅
                logger.error(f"SMTP error occurred: {str(e)}")
                response_data = {"success": 0, "message": f"SMTP error occurred: {str(e)}"}
            except Exception as e:
                # 예상치 못한 오류 로깅
                logger.error(f"Unexpected error: {str(e)}")
                response_data = {"success": 0, "message": f"An unexpected error occurred: {str(e)}"}

            # 실패 응답 직렬화
            response_serializer = EmailResponseSerializer(data=response_data)

            # 실패 응답 직렬화가 유효한지 확인
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 직렬화 오류 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)