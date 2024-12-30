from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging
import jwt

from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.validate_service import ValidateService
from apps.toro_auth.interface.serializers import ValidateRequestSerializer, ValidateResponseSerializer

logger = logging.getLogger(__name__)

class ValidateView(APIView):
    permission_classes = [AllowAny]
    validate_service: ValidateService = Provide[Container.validate_service]

    @swagger_auto_schema(
        request_body=ValidateRequestSerializer,
        responses={
            200: ValidateResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            401: "유효하지 않은 토큰입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="토큰 검증",
        operation_description="Access Token의 유효성을 검증하는 API입니다.",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        try:
            # 요청 데이터 검증
            serializer = ValidateRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Access Token 가져오기
            token = serializer.validated_data["access_token"]

            # Access Token 검증
            result = self.validate_service.validate_access_token(token)
            return self._success_response(result)

        except jwt.ExpiredSignatureError:
            logger.warning("Expired Access Token")
            return self._error_response("Access Token이 만료되었습니다.", status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidTokenError:
            logger.warning("Invalid Access Token")
            return self._error_response("유효하지 않은 Access Token입니다.", status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _success_response(self, data):
        """성공 응답 생성"""
        return Response({
            "success": 1,
            "message": "Access Token이 유효합니다.",
            "data": data
        }, status=status.HTTP_200_OK)

    def _error_response(self, message, status_code):
        """오류 응답 생성"""
        return Response({
            "success": 0,
            "message": message
        }, status=status_code)
