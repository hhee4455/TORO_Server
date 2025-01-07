from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging
import jwt

from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.update_refresh_token_service import UpdateRefreshTokenService
from apps.toro_auth.interface.serializers import (
    UpdateRefreshTokenRequestSerializer, 
    UpdateRefreshTokenResponseSerializer
)

logger = logging.getLogger(__name__)


class UpdateRefreshTokenView(APIView):
    """
    Refresh Token을 사용해 새로운 Access Token을 발급하는 API.
    """
    permission_classes = [AllowAny]
    update_refresh_token_service: UpdateRefreshTokenService = Provide[Container.update_refresh_token_service]

    @swagger_auto_schema(
        request_body=UpdateRefreshTokenRequestSerializer,
        responses={
            200: UpdateRefreshTokenResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            401: "유효하지 않은 Refresh Token입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="Access Token 갱신",
        operation_description="Refresh Token을 검증하여 새로운 Access Token을 발급합니다.",
        tags=["Token"]
    )
    def post(self, request, update_refresh_token_service: UpdateRefreshTokenService = update_refresh_token_service, *args, **kwargs):
        try:
            # 요청 데이터 검증
            serializer = UpdateRefreshTokenRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Refresh Token 가져오기
            refresh_token = serializer.validated_data["refresh_token"]
            logger.debug(f"Received Refresh Token: {refresh_token}")

            # Refresh Token 검증 및 Access Token 생성
            new_access_token = update_refresh_token_service.refresh_access_token(refresh_token)
            logger.info("Access Token successfully refreshed.")
            return self._success_response(new_access_token)

        except jwt.ExpiredSignatureError:
            logger.warning("Refresh Token has expired.")
            return self._error_response("Refresh Token이 만료되었습니다.", status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidTokenError:
            logger.warning("Invalid Refresh Token.")
            return self._error_response("유효하지 않은 Refresh Token입니다.", status.HTTP_401_UNAUTHORIZED)

        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return self._error_response(str(e), status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _success_response(self, access_token: str):
        """성공 응답 생성"""
        return Response({
            "success": 1,
            "message": "Access Token이 갱신되었습니다.",
            "data": {"access_token": access_token}
        }, status=status.HTTP_200_OK)

    def _error_response(self, message, status_code):
        """오류 응답 생성"""
        return Response({
            "success": 0,
            "message": message
        }, status=status_code)
