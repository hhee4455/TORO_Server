from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging

from apps.toro_auth.interface.serializers import LoginRequestSerializer, LoginResponseSerializer
from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.login_service import LoginService

logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]
    login_service: LoginService = Provide[Container.login_service]

    @swagger_auto_schema(
        request_body=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="로그인",
        operation_description="로그인을 요청하는 API입니다.",
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 로그인 서비스 호출
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            logger.info(f"Login attempt for email: {email}")

            result = self.login_service.login_user(email=email, password=password)
            return self._success_response(result)

        except ValueError as e:
            return self._error_response(str(e), status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _success_response(self, data):
        """성공 응답 생성"""
        return Response({"success": 1, "data": data}, status=status.HTTP_200_OK)

    def _error_response(self, message, status_code):
        """오류 응답 생성"""
        return Response({"success": 0, "message": message}, status=status_code)
