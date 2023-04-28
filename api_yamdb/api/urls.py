from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, APISignup, ApiGetToken
app_name = 'api'
router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', ApiGetToken.as_view(), name='get_token'),
    path('api/v1/auth/signup/', APISignup.as_view(), name='sighup'),
]