import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.toro_auth.interface.serializers import EmailRequestSerializer, EmailResponseSerializer
from apps.toro_auth.application.service.email_service import EmailService
from rest_framework.permissions import AllowAny
import smtplib
from dependency_injector.wiring import inject, Provide
from apps.toro_auth.di.containers import Container
from rest_framework.exceptions import ValidationError

# 로거 설정
logger = logging.getLogger(__name__)

class EmailRequestView(APIView):
    permission_classes = [AllowAny]

    @inject
    def __init__(self, email_service: EmailService = Provide[Container.email_service], **kwargs):
        super().__init__(**kwargs)
        self.email_service = email_service

    @swagger_auto_schema(
        request_body=EmailRequestSerializer,
        responses={200: EmailResponseSerializer, 400: 'Bad Request'},
        operation_summary="이메일 인증(전송)",
        operation_description="이메일 인증 요청 API",
    )
    def post(self, request, *args, **kwargs):
        serializer = EmailRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            logger.info(f"Received email: {email}")

            try:
                # 이메일 전송 시도
                self.email_service.send_email(email)

                # 성공 응답
                response_data = {"success": 1, "message": "이메일이 성공적으로 전송 되었습니다."}
                return Response(response_data, status=status.HTTP_200_OK)

            except ValidationError as e:
                # ValidationError 메시지만 추출
                message = e.detail if hasattr(e, 'detail') else str(e)
                if isinstance(message, list):
                    message = message[0]
                logger.error(f"Validation error: {message}")
                return Response(
                    {"success": 0, "message": message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            except smtplib.SMTPException as e:
                # SMTP 오류 처리
                logger.error(f"SMTP error occurred: {str(e)}")
                return Response(
                    {"success": 0, "message": "SMTP 오류가 발생했습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            except Exception as e:
                # 예상치 못한 오류 처리
                logger.error(f"Unexpected error: {str(e)}")
                return Response(
                    {"success": 0, "message": "서버 내부 오류가 발생했습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 직렬화 오류 처리
        return Response(
            {"success": 0, "message": "유효하지 않은 요청입니다.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
