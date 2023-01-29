from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post,Comment
User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','title')

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(queryset = User.objects.all(),view_name='owner-detail',many=False)
    comments= serializers.HyperlinkedRelatedField(queryset = Comment.objects.all(),view_name='comment-detail',many=True)
    class Meta:
        model = Post
        fields = ('id','title','owner','custom_id','category','publish_date','last_updated','comments')
