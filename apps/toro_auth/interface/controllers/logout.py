from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging

from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.logout_service import LogoutService
from apps.toro_auth.interface.serializers import LogoutRequestSerializer, LogoutResponseSerializer

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    logout_service: LogoutService = Provide[Container.logout_service]

    @swagger_auto_schema(
        request_body=LogoutRequestSerializer,
        responses={
            200: LogoutResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="로그아웃",
        operation_description="로그아웃을 요청하는 API입니다.",
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        try:
            logger.debug(f"Logout request data: {request.data}")
            serializer = LogoutRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            token = serializer.validated_data["refresh_token"]
            logger.info(f"Logout attempt for token: {token}")

            result = self.logout_service.logout_user(token=token)
            return self._success_response(result)

        except KeyError as e:
            logger.error(f"Missing token in request: {str(e)}")
            return self._error_response("토큰이 요청에 포함되지 않았습니다.", status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            logger.warning(f"Invalid token during logout: {str(e)}")
            return self._error_response(str(e), status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _success_response(self, data):
        """성공 응답 생성"""
        return Response({"success": 1, "message": data}, status=status.HTTP_200_OK)

    def _error_response(self, message, status_code):
        """오류 응답 생성"""
        return Response({"success": 0, "message": message}, status=status_code)
