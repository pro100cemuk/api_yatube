from rest_framework import serializers

from posts.models import Comment, Group, Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('id', 'author', 'created', 'post')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    comments = CommentSerializer(required=False, many=True)
    group = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date',
                  'comments')
        model = Post
        read_only_fields = ('id', 'image', 'group', 'pub_date', 'comments')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group
