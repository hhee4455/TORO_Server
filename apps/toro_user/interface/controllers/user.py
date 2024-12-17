from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from apps.toro_user.application.service.user_service import UserService


class UserView(APIView):
    """
    사용자 정보를 조회하는 API 뷰.
    사용자의 email을 기반으로 정보를 조회합니다.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="사용자 조회",
        operation_description="이메일로 사용자 정보를 조회합니다.",
    )
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')

        if not email:
            return Response({'error': '이메일을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        user_service = UserService()
        user_data = user_service.get_user_by_email(email)

        if user_data:
            return Response({'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
