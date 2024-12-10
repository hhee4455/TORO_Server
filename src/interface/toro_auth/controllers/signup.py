from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from dependency_injector.wiring import inject, Provide
from apps.toro_auth.di.containers import Container
from apps.toro_auth.interface.serializers import SignupRequestSerializer, SignupResponseSerializer
from apps.toro_auth.application.service.signup_service import SignupService
from rest_framework.permissions import AllowAny

class SignupView(APIView):
    permission_classes = [AllowAny]

    @inject
    def __init__(self, signup_service: SignupService = Provide[Container.login_service], **kwargs):
        super().__init__(**kwargs)
        self.signup_service = signup_service

    @swagger_auto_schema(
        request_body=SignupRequestSerializer,
        responses={
            201: SignupResponseSerializer,
            400: "잘못된 요청 데이터입니다.",
            500: "서버 내부 오류입니다.",
        },
        operation_summary="회원가입",
        operation_description="회원가입을 요청하는 API입니다."
    )
    def post(self, request, *args, **kwargs):
        serializer = SignupRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.signup_service.signup_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                name=serializer.validated_data["name"]
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _error_response(self, message, status_code):
        return Response({"success": 0, "message": message}, status=status_code)
    