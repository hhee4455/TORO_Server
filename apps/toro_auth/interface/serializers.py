from rest_framework import serializers

class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class EmailResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    code = serializers.CharField(required=False, max_length=6)

class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    name = serializers.CharField(required=True, max_length=100)

class SignupResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

class LoginResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()