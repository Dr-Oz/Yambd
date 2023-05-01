from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, APISignup, ApiGetToken
app_name = 'api'
router = SimpleRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', ApiGetToken.as_view(), name='get_token'),
    path('api/v1/auth/signup/', APISignup.as_view(), name='sighup'),
]