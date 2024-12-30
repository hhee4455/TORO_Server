from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging

from apps.toro_auth.di.containers import Container
from apps.toro_auth.interface.serializers import SignupRequestSerializer, SignupResponseSerializer
from apps.toro_auth.application.service.signup_service import SignupService

logger = logging.getLogger(__name__)

class SignupView(APIView):
    permission_classes = [AllowAny]
    signup_service: SignupService = Provide[Container.signup_service]

    @swagger_auto_schema(
        request_body=SignupRequestSerializer,
        responses={
            201: SignupResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="회원가입",
        operation_description="회원가입을 요청하는 API입니다.",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SignupRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 회원가입 서비스 호출
            validated_data = serializer.validated_data
            logger.info(f"Signup attempt for email: {validated_data['email']}")

            result = self.signup_service.signup_user(
                email=validated_data["email"],
                password=validated_data["password"],
                name=validated_data["name"]
            )
            return self._success_response(result)

        except Exception as e:
            logger.error(f"Unexpected error during signup: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _success_response(self, data):
        """성공 응답 생성"""
        return Response({"success": 1, "data": data}, status=status.HTTP_201_CREATED)

    def _error_response(self, message, status_code):
        """오류 응답 생성"""
        return Response({"success": 0, "message": message}, status=status_code)
