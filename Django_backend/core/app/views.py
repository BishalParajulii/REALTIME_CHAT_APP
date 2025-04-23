from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer , SignUpSerializer


def get_auth_for_user(user):
    token = RefreshToken.for_user(user)
    return {
        'user': UserSerializer(user).data,
        'token' : {
            'refresh' : str(token),
            'access' : str(token.access_token)
        }
    }


class SignInView(APIView):
    permission_classes = [AllowAny]  # Fixed: should be `permission_classes`

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password required.'}, status=400)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=401)

        user_data = get_auth_for_user(user)
        return Response(user_data)



class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self , request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)


        user_data = get_auth_for_user(user)
        return Response(user_data)