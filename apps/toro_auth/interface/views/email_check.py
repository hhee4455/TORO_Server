from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.toro_auth.interface.serializers import EmailRequestSerializer, EmailResponseSerializer
from apps.toro_auth.domain.entity.account import Account
from rest_framework.permissions import AllowAny

class CheckCodeView(APIView):
    """
    인증 코드 검증 요청을 처리하는 API 뷰.
    사용자가 입력한 인증 코드가 이메일로 발송된 코드와 일치하는지 확인합니다.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="인증 코드 검증 API",
        request_body=EmailRequestSerializer,  # EmailRequestSerializer 사용
        responses={200: EmailResponseSerializer, 400: 'Invalid code.', 404: 'Account not found.'}
    )
    def post(self, request, *args, **kwargs):
        """
        POST 요청을 처리하여 이메일 인증 코드를 검증한다.
        사용자가 제공한 이메일 주소와 인증 코드가 유효한지 확인한다.
        """
        # 이메일과 인증 코드만 받아서 Serializer로 변환
        serializer = EmailRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data.get("code")
        else:
            return Response({"message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        if not email or not code:
            return Response({"message": "Email and code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 이메일로 해당 계정을 찾기
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"message": "Account with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # 인증 코드 확인
        if account.verification_code == code:
            # 인증 코드가 일치하면 인증 완료 처리
            account.verification_code = None  # 인증 후 코드 제거
            account.save()

            # 응답 DTO 생성
            response_data = {"success": 1, "message": "Email verified successfully."}
            response_serializer = EmailResponseSerializer(data=response_data)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
