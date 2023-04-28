from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from review.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from .permissions import (AdminModeratorAuthorPermission, AdminOnly,
                          IsAdminUserOrReadOnly)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

class APISignup(APIView):
    """
        Получить код подтверждения на переданный email. Права доступа: Доступно без
        токена. Использовать имя 'me' в качестве username запрещено. Поля email и
        username должны быть уникальными. Пример тела запроса:
        {
            "email": "string",
            "username": "string"
        }
        """

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена. Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)
