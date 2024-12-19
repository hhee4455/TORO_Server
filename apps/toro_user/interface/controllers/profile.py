from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import inject, Provide
from apps.toro_user.di.containers import Container

from apps.toro_user.application.service.profile_service import ProfileService

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    @inject
    def __init__(self, profile_service: ProfileService = Provide[Container.profile_service], **kwargs):
        super().__init__(**kwargs)
        self.profile_service = profile_service

    @swagger_auto_schema(
        responses={
            200: "프로필 이미지 URL이 반환됩니다.",
            401: "인증되지 않은 사용자입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="프로필 이미지 조회",
        operation_description="사용자의 프로필 이미지를 반환하는 API입니다."
    )
    def get(self, request, *args, **kwargs):
        try:
            # 현재 사용자로부터 프로필 이미지 가져오기
            profile_image_url = self.profile_service.get_profile_picture(request.user)

            return Response(
                {"success": 1, "message": "프로필 이미지가 반환되었습니다.", "profile_image": profile_image_url},
                status=status.HTTP_200_OK
            )
        except ValueError as e:  # 사용자 프로필이 없거나 잘못된 요청
            return Response(
                {"success": 0, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:  # 서버 오류
            return Response(
                {"success": 0, "message": f"서버 내부 오류: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
