from rest_framework import serializers
from .models import UserPost, Post

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'