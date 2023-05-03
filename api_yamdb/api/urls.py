from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, APISignup, ApiGetToken, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet
app_name = 'api'
router = SimpleRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', ApiGetToken.as_view(), name='get_token'),
    path('api/v1/auth/signup/', APISignup.as_view(), name='sighup'),
]