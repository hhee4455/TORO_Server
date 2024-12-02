from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.toro_auth.interface.serializers import SignupRequestSerializer, SignupResponseSerializer
from apps.toro_auth.application.service.signup_service import SignupService
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError

class SignupView(APIView):
    """회원가입 API 뷰."""
    permission_classes = [AllowAny]

    def __init__(self, signup_service: SignupService = None, **kwargs):
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
        """회원가입 POST 요청 처리."""
        serializer = SignupRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.signup_service.signup_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                name=serializer.validated_data["name"]
            )
            response_serializer = SignupResponseSerializer(data=result)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return self._error_response(e.detail, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _error_response(self, message, status_code):
        return Response({"success": 0, "message": message}, status=status_code)
