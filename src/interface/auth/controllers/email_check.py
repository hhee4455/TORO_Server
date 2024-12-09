from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.toro_auth.application.service.email_service import EmailService
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

class CheckCodeView(APIView):
    """
    이메일 인증 번호 확인을 처리하는 API 뷰.
    사용자가 입력한 인증 번호를 검증합니다.
    """

    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="이메일 인증(확인)",
        operation_description="이메일 확인 요청 API",
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'error': '이메일과 인증번호를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        email_service = EmailService()
        is_verified = email_service.verify_code(email, code)

        if is_verified:
            return Response({'message': '인증에 성공했습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '인증번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
