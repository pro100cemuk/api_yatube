from rest_framework import serializers

from posts.models import Comment, Group, Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('id', 'author', 'created', 'post')

    def update(self, instance, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.StringRelatedField(read_only=True, required=False)
    group = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Group.objects.all(),
                                         required=False)
    pub_date = serializers.DateTimeField(read_only=True, required=False)
    comments = CommentSerializer(required=False, many=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date',
                  'comments')
        model = Post

    def create(self, validated_data):
        if 'comments' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        else:
            comments = validated_data.pop('comments')
            post = Post.objects.create(**validated_data)
            for comment in comments:
                current_comment, status = Comment.objects.get_or_create(
                    **comment)
                Comment.objects.create(
                    text=current_comment, post=post)
            return post

    def update(self, instance, validated_data):
        if 'comments' not in validated_data:
            instance.text = validated_data.get('text', instance.text)
            instance.group = validated_data.get('group', instance.group)
            instance.save()
            return instance
        else:
            comments_data = validated_data.pop('comments')
            instance.text = validated_data.get('text', instance.text)
            instance.group = validated_data.get('group', instance.group)
            lst = []
            for comment in comments_data:
                current_comment, status = Comment.objects.get_or_create(
                    **comment)
                lst.append(current_comment)
            instance.comments.set(lst)
            instance.save()
            return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group
