from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

# 1. User Serializer (To show who posted)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# 2. Post Serializer (To show the actual post)
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) # Nest the user info inside the post

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'date_posted', 'author']