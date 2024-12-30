from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import inject, Provide
from apps.toro_user.di.containers import Container
from apps.toro_user.application.service.profile_service import ProfileService
from apps.toro_user.interface.serializers import ProfileRequestSerializer
import logging

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    
    permission_classes = [AllowAny]

    @inject
    def __init__(self, profile_service: ProfileService = Provide[Container.profile_service], **kwargs):
        super().__init__(**kwargs)
        self.profile_service = profile_service

    @swagger_auto_schema(
        request_body=ProfileRequestSerializer,
        responses={
            200: "프로필 이미지 URL이 반환됩니다.",
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="프로필 이미지 조회",
        operation_description="사용자의 리프레시 토큰으로 프로필 이미지를 반환하는 API입니다.",
        tags=["Profile"]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = ProfileRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 요청 데이터에서 토큰 추출
            token = serializer.validated_data["token"]
            logger.info(f"Token received for profile picture: {token}")

            # ProfileService에서 프로필 이미지 URL 가져오기
            profile_image_url = self.profile_service.get_profile_picture(token)

            return self._success_response(
                message="프로필 이미지가 반환되었습니다.",
                data={"profile_image": profile_image_url}
            )
        except ValueError as e:  # 사용자 인증 오류
            logger.error(f"Authentication error: {str(e)}")
            return self._error_response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # 서버 오류
            logger.error(f"Unexpected error: {str(e)}")
            return self._error_response("서버 내부 오류가 발생했습니다.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _success_response(self, message, data=None):
        """
        성공 응답을 생성하는 헬퍼 함수.
        """
        response_data = {"success": 1, "message": message}
        if data:
            response_data.update(data)
        return Response(response_data, status=status.HTTP_200_OK)

    def _error_response(self, message, status_code):
        """
        오류 응답을 생성하는 헬퍼 함수.
        """
        return Response({"success": 0, "message": message}, status=status_code)
