# Django Import
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

# Rest Framework JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Local Import
from base.models import *
from base.serializers import UserSerializer, UserSerializerWithToken


# # JWT Views
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        data |= serializer
        print(data)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['message'] = 'TEST TOKEN MESSAGE'
        print(f'{token = }')
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# SHOP API
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/<id>',
        '/api/users',
        '/api/users/register',
        '/api/users/login',
        '/api/users/profile',
    ]
    return Response(routes)


@api_view(['POST'])
def register_user(request):
    data = request.data
    print(data)
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            password=make_password(data['password']),
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    except:
        message = {"detail": "User with this email is already registered"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request: WSGIRequest) -> Response:
    user = request.user
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request: WSGIRequest) -> Response:
    user = request.user
    data = request.data
    serializer = UserSerializerWithToken(user, many=False)
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request: WSGIRequest) -> Response:
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request: WSGIRequest, pk: int) -> Response:
    users = User.objects.get(pk=pk)
    serializer = UserSerializer(users, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request: WSGIRequest, pk: int) -> Response:
    data = request.data

    user = User.objects.get(pk=pk)
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request: WSGIRequest, pk: int) -> Response:
    user = User.objects.get(pk=pk)
    name = user.first_name or user.email or user.username
    user.delete()

    return Response(f'The user {name} has been deleted')
