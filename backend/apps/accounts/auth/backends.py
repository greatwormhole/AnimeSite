from django.contrib.auth.backends import BaseBackend

class EmailAuthenticationBackend(BaseBackend):
    """
    Authenticating user through email
    """
    def authenticate(self, request, **kwargs):
        pass
    
    