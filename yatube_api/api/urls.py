from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

v1_router = SimpleRouter()
v1_router.register(r'api/v1/posts', PostViewSet)
v1_router.register(r'api/v1/groups', GroupViewSet)
v1_router.register(r'api/v1/posts/(?P<post_id>[^/.]+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(v1_router.urls)),
]
