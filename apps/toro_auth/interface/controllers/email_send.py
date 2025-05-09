import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from smtplib import SMTPException
from dependency_injector.wiring import Provide
from rest_framework.exceptions import ValidationError

from apps.toro_auth.di.containers import Container
from apps.toro_auth.interface.serializers import EmailRequestSerializer, EmailResponseSerializer
from apps.toro_auth.application.service.email_service import EmailService

logger = logging.getLogger(__name__)

class EmailRequestView(APIView):
    permission_classes = [AllowAny]
    email_service: EmailService = Provide[Container.email_service]

    @swagger_auto_schema(
        request_body=EmailRequestSerializer,
        responses={
            200: EmailResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="이메일 전송",
        operation_description="이메일 전송을 요청하는 API입니다.",
        tags=["Email"]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data["email"]
            logger.info(f"Received email: {email}")

            self.email_service.send_email(email)
            return self._success_response("이메일이 성공적으로 전송 되었습니다.")

        except ValidationError as e:
            return self._handle_validation_error(e)

        except SMTPException as e:
            return self._handle_smtp_error(e)

        except Exception as e:
            return self._handle_unexpected_error(e)

    def _success_response(self, message):
        """성공 응답 생성"""
        response_data = {"success": 1, "message": message}
        return Response(response_data, status=status.HTTP_200_OK)

    def _handle_validation_error(self, error):
        """ValidationError 처리"""
        message = error.detail if hasattr(error, 'detail') else str(error)
        if isinstance(message, list):
            message = message[0]
        logger.error(f"Validation error: {message}")
        response_data = {"success": 0, "message": message}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def _handle_smtp_error(self, error):
        """SMTPException 처리"""
        logger.error(f"SMTP error occurred: {str(error)}")
        response_data = {"success": 0, "message": "SMTP 오류가 발생했습니다."}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _handle_unexpected_error(self, error):
        """예상치 못한 오류 처리"""
        logger.error(f"Unexpected error: {str(error)}")
        response_data = {"success": 0, "message": "서버 내부 오류가 발생했습니다."}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
