from .models import Blog, Like, Comment
from authenticate.models import User
from rest_framework import serializers
from authenticate.serializer import RegisterSerializer
from taggit.serializers import TaggitSerializer,TagListSerializerField


class BlogSerializer(TaggitSerializer,serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    tags=TagListSerializerField()
    class Meta:
        model = Blog
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
