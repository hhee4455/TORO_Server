from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.toro_auth.interface.serializers import LoginRequestSerializer, LoginResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import inject, Provide
from apps.toro_auth.di.containers import Container
from apps.toro_auth.application.service.login_service import LoginService


class LoginView(APIView):
    permission_classes = [AllowAny]

    @inject
    def __init__(self, login_service: LoginService = Provide[Container.login_service], **kwargs):
        super().__init__(**kwargs)
        self.login_service = login_service
    
    @swagger_auto_schema(
        request_body=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="로그인",
        operation_description="로그인을 요청하는 API입니다."
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.login_service.login_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _error_response(self, message, status_code):
        return Response({"success": 0, "message": message}, status=status_code)
    