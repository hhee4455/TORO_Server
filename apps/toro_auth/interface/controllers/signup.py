from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.interface.serializers.serializers import SignupRequestSerializer, SignupResponseSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpRequest
from injector import inject

class SignupView(APIView):
    """
    회원가입 요청을 처리하는 API 뷰.
    """

    permission_classes = [AllowAny]  # 모든 사용자 접근 허용

    @inject
    def __init__(self, signup_service: SignupService = None, **kwargs):
        """
        SignupView 생성자.

        Args:
            signup_service (SignupService): 의존성 주입된 SignupService 객체
        """
        super().__init__(**kwargs)
        self.signup_service = signup_service

    @swagger_auto_schema(
        request_body=SignupRequestSerializer,
        responses={201: SignupResponseSerializer},
        operation_summary="회원가입",
        operation_description="회원가입을 요청하는 API입니다."
    )
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        회원가입 POST 요청을 처리하는 메서드.

        Args:
            request (Request): 클라이언트로부터의 HTTP 요청 객체

        Returns:
            Response: 처리 결과에 따른 HTTP 응답
        """
        # 요청 데이터 직렬화 및 유효성 검사
        serializer = SignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            name = serializer.validated_data["name"]

            try:
                # 회원가입 서비스 호출
                result = self.signup_service.signup_user(email, password, name)
                response_data = {
                    "success": 1,
                    "message": result["message"],
                    "access_token": result["access_token"],
                    "refresh_token": result["refresh_token"]
                }

                # 응답 직렬화
                response_serializer = SignupResponseSerializer(data=response_data)
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                return Response(
                    {"success": 0, "message": str(e.detail)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"success": 0, "message": f"Unexpected error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 유효하지 않은 입력 데이터 처리
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
