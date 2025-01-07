from rest_framework import serializers

#이메일 요청 시리얼라이저
class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(required=False, max_length=6)
    
class EmailResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    code = serializers.CharField(required=False, max_length=6)

#회원가입 요청 시리얼라이저
class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    name = serializers.CharField(required=True, max_length=100)
    phone = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)

class SignupResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()

#로그인 요청 시리얼라이저
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

class LoginResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

#로그아웃 요청 시리얼라이저
class LogoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

class LogoutResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()


#토큰 검증 요청 시리얼라이저
class ValidateRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)

class ValidateResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()

#토큰 갱신 요청 시리얼라이저
class UpdateRefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

class UpdateRefreshTokenResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()
    access_token = serializers.CharField()