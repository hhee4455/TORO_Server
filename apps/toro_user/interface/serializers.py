from rest_framework import serializers

class UserRequestSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True, max_length=100)
    bio = serializers.CharField(required=False, allow_blank=True)
    is_public = serializers.BooleanField(required=False, default=False)
    location = serializers.CharField(required=False, max_length=100, allow_blank=True)
    available_for_work = serializers.BooleanField(required=False, default=False)
    fieldwork_availability = serializers.CharField(required=False, max_length=100, allow_blank=True)
    field = serializers.CharField(required=False, max_length=100, allow_blank=True)
    profile_picture = serializers.URLField(required=False) 


class UserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    nickname = serializers.CharField()
    bio = serializers.CharField(allow_blank=True, required=False)
    is_public = serializers.BooleanField()
    last_seen = serializers.DateTimeField()
    location = serializers.CharField(allow_blank=True, required=False)
    available_for_work = serializers.BooleanField()
    follower_count = serializers.IntegerField()
    fieldwork_availability = serializers.CharField(allow_blank=True, required=False)
    field = serializers.CharField(allow_blank=True, required=False)
    profile_picture = serializers.URLField(allow_blank=True, required=False) 
    is_active = serializers.BooleanField()
    account_id = serializers.UUIDField()

class ProfileRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=True)

class ProfileResponseSerializer(serializers.Serializer):
    profile_picture = serializers.URLField(allow_blank=True, required=False)