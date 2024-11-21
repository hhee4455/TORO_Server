from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SignupView(APIView):
    response = {
        'success': 1,
        'message': '회원가입에 성공했습니다.'
    }