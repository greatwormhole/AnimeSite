from rest_framework.authentication import BaseAuthentication, get_authorization_header
from web_django.settings import JWT_TOKEN_CONFIGURATION as settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import HTTP_HEADER_ENCODING

from jwt.exceptions import ExpiredSignatureError, DecodeError

from apps.accounts.models import AuthUser
from .tokens import DecodeJWTToken

class JWTAuthentication(BaseAuthentication):
    
    """
    Self-written REST Framework JWT Authentication class
    """
    
    # Edit JWT_AUTH_HEADER key in jwt settings to edit auth header prefix
    keyword = settings.get('JWT_AUTH_HEADER').lower()
    
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode(HTTP_HEADER_ENCODING):
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            raw_token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')
        
        try:
            jwt_access_token = DecodeJWTToken(raw_token)
        except ExpiredSignatureError:
            return None
        except DecodeError:
            raise AuthenticationFailed('Token fields are wrong')
        
        return self.authenticate_credentials(jwt_access_token)
    
    def authenticate_credentials(self, token):
        
        try:
            user = AuthUser.objects.get(username=token.username)
        except AuthUser.DoesNotExist:
            return None
        
        return (user, token)
    
    def authenticate_header(self, request):
        return self.keyword