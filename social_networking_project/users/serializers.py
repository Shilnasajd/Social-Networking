from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest
from rest_framework.pagination import PageNumberPagination


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
    
class UserSearchPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: set a maximum limit for items per page

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_name = serializers.SerializerMethodField()
    to_user_name = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user_name', 'to_user_name']  # Include to_user_name instead of to_user

    def get_from_user_name(self, obj):
        return obj.from_user.username

    def get_to_user_name(self, obj):
        return obj.to_user.username
                            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']