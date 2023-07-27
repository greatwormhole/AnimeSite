from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    )
from rest_framework.permissions import IsAdminUser

from .models import AuthUser
from .serializers import UserSerializer
from apps.accounts.auth.tokens import EncodeJWTToken, DecodeJWTToken

from jwt.exceptions import ExpiredSignatureError
from datetime import datetime as dt

class UserListView(APIView):

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def get(self, request):

        users = AuthUser.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

class RefreshJWTTokenView(APIView):

    def post(self, request):
        
        raw_refresh_token = request.data.get('refresh', None)

        if raw_refresh_token is None:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        try:
            jwt_refresh_token = DecodeJWTToken(raw_refresh_token)
        except ExpiredSignatureError:
            return Response(status=HTTP_401_UNAUTHORIZED)
        data = {
            'access': EncodeJWTToken(
                username=jwt_refresh_token.username,
                email=jwt_refresh_token.email,
                token_type='access',
            ).encode()
        }

        response = Response(data=data, status=HTTP_200_OK)

        return response

class LoginUserView(APIView):

    def post(self, request):
        
        credentials = request.data

        user = authenticate(
            request,
            username=credentials.get('username', None),
            password=credentials.get('password', None)
        )
        
        if user is None:
            return Response(status=HTTP_404_NOT_FOUND)

        jwt_access_token = EncodeJWTToken(
            username=user.get_username(),
            email=getattr(user, user.get_email_field_name(), 'MissingEmail'),
            token_type='access',
        ).encode()
        
        jwt_refresh_token = EncodeJWTToken(
            username=user.get_username(),
            email=getattr(user, user.get_email_field_name(), 'MissingEmail'),
            token_type='refresh',
        ).encode()

        response = Response(
            data={
                'refresh': jwt_refresh_token,
                'access': jwt_access_token,
            },
            status=HTTP_200_OK
        )

        return response