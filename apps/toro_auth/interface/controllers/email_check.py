from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import inject, Provide

from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.email_service import EmailService
from apps.toro_auth.interface.serializers import EmailRequestSerializer, EmailResponseSerializer

class CheckCodeView(APIView):
    permission_classes = [AllowAny]
    email_service: EmailService = Provide[Container.email_service]

    @swagger_auto_schema(
        request_body=EmailRequestSerializer,
        responses={
            200: EmailResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="이메일 인증 번호 확인",
        operation_description="사용자가 입력한 이메일 인증 번호를 확인하는 API입니다.",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        serializer = EmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        is_verified = self.email_service.verify_code(email, code)
        message = '인증에 성공했습니다.' if is_verified else '인증번호가 일치하지 않습니다.'
        return Response(
            {'success': int(is_verified), 'message': message},
            status=status.HTTP_200_OK if is_verified else status.HTTP_400_BAD_REQUEST
        )
