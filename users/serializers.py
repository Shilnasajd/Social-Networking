from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserSearchSerializer(serializers.Serializer):
    search_keyword = serializers.CharField(max_length=255)

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_name = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'from_user_name']  # Add other fields as needed

    def get_from_user_name(self, obj):
        from_user_id = obj.from_user_id
        try:
            from_user = User.objects.get(id=from_user_id)
            return from_user.username
        except User.DoesNotExist:
            return None
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']