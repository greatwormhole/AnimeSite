from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    )
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)

from .models import AuthUser
from .serializers import *
from apps.accounts.auth.tokens import EncodeJWTToken, DecodeJWTToken
from .permissions import IsCurrentUser

from jwt.exceptions import ExpiredSignatureError

class RefreshJWTTokenView(APIView):
    
    permission_classes = [IsAuthenticated, ]

    def post(self, request) -> Response:
        
        raw_refresh_token = request.data.get('refresh', None)

        if raw_refresh_token is None:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        try:
            jwt_refresh_token = DecodeJWTToken(raw_refresh_token)
        except ExpiredSignatureError:
            return Response({'detail': 'Refresh token has been expired'}, status=HTTP_401_UNAUTHORIZED)
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

    permission_classes = [AllowAny, ]
    
    def post(self, request: Request) -> Response:
        
        credentials = request.data

        user = authenticate(
            request,
            username=credentials.get('username', None),
            password=credentials.get('password', None)
        )
        
        if user is None:
            return Response({'detail': "User with such credentials doesn't exist"}, status=HTTP_404_NOT_FOUND)

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
    
class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    
    queryset = AuthUser.objects.all()
    lookup_field = 'username'
    
    def get_permissions(self):
        match self.action:
            case 'list':
                permission_classes = [IsAdminUser]
            case 'destroy':
                permission_classes = [IsAdminUser]
            case 'register':
                permission_classes = [AllowAny]
            case _:
                permission_classes = [IsAdminUser, IsCurrentUser]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return AdminUserSerializer
            case 'change_password':
                return PasswordChangeSerializer
            case 'register':
                return RegisterSerializer
            case _:
                return UserSerializer
            
    def get_object(self):
        return 
            
    @action(methods=['PATCH'], detail=True, url_path='change-password', url_name='change_password')
    def change_password(self, request: Request, pk: int | None = None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():  
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {
                        'old_password': ['Wrong password'],
                    },
                    status=HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response(
                {
                    'message': 'Password has been changed successfully',
                },
                status=HTTP_200_OK
            )
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False)
    def register(self, request: Request):
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'message': 'Registration successful'
                },
                status=HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=HTTP_400_BAD_REQUEST
        )
        