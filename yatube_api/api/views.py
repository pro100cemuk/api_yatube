from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(pk=post_id)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.request.query_params.get('comment_id', None)
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def retrieve(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        post_id = self.kwargs.get('post_id')
        post = Comment.objects.filter(post_id=post_id)
        comment = get_object_or_404(post, id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        post_id = self.kwargs.get('post_id')
        post = Comment.objects.filter(post_id=post_id)
        comment = get_object_or_404(post, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        post_id = self.kwargs.get('post_id')
        post = Comment.objects.filter(post_id=post_id)
        comment = get_object_or_404(post, id=comment_id)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
