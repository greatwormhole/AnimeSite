from datetime import datetime as dt, timedelta as td
import jwt

from web_django.settings import JWT_TOKEN_CONFIGURATION as settings

class EncodeJWTToken:
    
    """
    Basic JWT Token encoding class. Add required fields to __init__ to initialize
    them and pass to encoder.
    """
    
    def __init__(
        self,
        username: str,
        email: str,
        token_type: str,
    ):
        self.username = username
        self.email = email
        if token_type == 'access':
            self.exp = int((dt.now() + settings.get('ACCESS_TOKEN_LIFETIME', '')).timestamp())
        elif token_type == 'refresh':
            self.exp = int((dt.now() + settings.get('REFRESH_TOKEN_LIFETIME', '')).timestamp())
    
    def encode(self):
        return jwt.encode(
            payload=self.to_payload(),
            key=self._signature_key(),
            algorithm=self._algorithm(),
        )
        
    def to_payload(self):
        return self.__dict__
    
    def _signature_key(self):
        return settings.get('SIGNATURE_KEY', '')

    def _algorithm(self):
        return settings.get('ENCODING_ALGORITHM', '')
    
class DecodeJWTToken:
    
    """
    Basic JWT Token decoding class.
    """
    
    def __init__(self, raw_token, return_expired: bool = False):
        self.data = jwt.decode(
            jwt=raw_token,
            key=settings.get('SIGNATURE_KEY', ''),
            algorithms=[settings.get('ENCODING_ALGORITHM', '')],
        )
        
        if False in map(lambda key: key in self.data.keys(), settings['JWT_KEYS'].keys()):
            raise jwt.exceptions.DecodeError("Token hasn't required fields")
        
    def __call__(self, *args, **kwargs):
        return self.is_expired
        
    @property
    def is_expired(self):
        return self.data['exp'] < int(dt.now().timestamp())
    
    @property
    def username(self):
        return self.data['username']
    
    @property
    def email(self):
        return self.data['email']