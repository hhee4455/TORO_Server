from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import Provide
import logging
import jwt

from apps.toro_user.di.containers import Container
from apps.toro_user.application.service.profile_service import ProfileService
from apps.toro_user.interface.serializers import ProfileRequestSerializer, ProfileResponseSerializer

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    permission_classes = [AllowAny]
    profile_service: ProfileService = Provide[Container.profile_service]

    @swagger_auto_schema(
        request_body=ProfileRequestSerializer,
        responses={
            200: ProfileResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            401: "유효하지 않은 토큰입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="프로필 조회",
        operation_description="사용자의 프로필 정보를 조회하는 API입니다.",
        tags=["User"]
    )
    def post(self, request, *args, **kwargs):
        try:
            # 요청 데이터 검증
            serializer = ProfileRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Access Token 가져오기
            token = serializer.validated_data["access_token"]

            # Access Token 검증
            result = self.profile_service.get_profile(token)
            return self._success_response(result)

        except jwt.ExpiredSignatureError:
            logger.warning("Expired Access Token")
            return self._error_response("Access Token이 만료되었습니다.", status.HTTP_401_UNAUTHORIZED)
        
        except jwt.InvalidTokenError:
            logger.error("Invalid Access Token")
            return self._error_response("유효하지 않은 Access Token입니다.", status.HTTP_401_UNAUTHORIZED)
        
        except ValueError as e:
            logger.error(f"Error: {str(e)}")
            return self._error_response(str(e), status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Internal Server Error: {str(e)}")
            return self._error_response("서버 내부 오류입니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _success_response(self, data):
        return Response(data, status=status.HTTP_200_OK)
    
    def _error_response(self, message, status_code):
        return Response({"message": message}, status=status_code)