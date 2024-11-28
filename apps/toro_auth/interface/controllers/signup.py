from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.interface.serializers.serializers import SignupRequestSerializer, SignupResponseSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

class SignupView(APIView):
    """
    회원가입 요청을 처리하는 API 뷰.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignupRequestSerializer,
        responses={201: SignupResponseSerializer},
        operation_summary="회원가입",
        operation_description="회원가입을 요청하는 API입니다."
    )
    def post(self, request, *args, **kwargs):
        # 요청 데이터 직렬화
        serializer = SignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            name = serializer.validated_data["name"]

            # 서비스 호출
            signup_service = SignupService()

            try:
                result = signup_service.signup_user(email, password, name)
                response_data = {
                    "success": 1,
                    "message": result["message"],
                    "access_token": result["access_token"],
                    "refresh_token": result["refresh_token"]
                }
                response_serializer = SignupResponseSerializer(data=response_data)

                # 응답 직렬화
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                return Response({"success": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"success": 0, "message": f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
