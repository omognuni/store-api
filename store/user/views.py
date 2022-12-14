from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    '''user 생성'''
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''user token 생성'''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
