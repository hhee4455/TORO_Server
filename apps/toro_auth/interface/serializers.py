from rest_framework import serializers

class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class EmailResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    code = serializers.CharField(required=False, max_length=6)