from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(v1_router.urls)),
]
