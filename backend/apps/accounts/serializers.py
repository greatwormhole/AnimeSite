from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField
)

from .models import AuthUser
from apps.main.models import Profile

class AdminUserSerializer(ModelSerializer):

    class Meta:
        model = AuthUser
        fields = '__all__'
        
class UserSerializer(ModelSerializer):

    class Meta:
        model = AuthUser
        exclude = ['password', 'groups', 'user_permissions']
        read_only_fields = ['date_created', 'is_staff', 'is_active']
        
class PasswordChangeSerializer(Serializer):
    old_password = CharField(required=True, write_only = True, max_length = 128)
    new_password =CharField(required=True, write_only = True, max_length = 128)
    
class RegisterSerializer(Serializer):
    username = CharField(max_length=150)
    email = EmailField()
    password = CharField(max_length=128)
    first_name = CharField(max_length=120)
    last_name = CharField(max_length=120)
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        user = AuthUser.objects.create(username=username, email=email, password=password)
        Profile.objects.create(user=user, first_name=first_name, last_name=last_name)
        
        return user

class LoginSerializer(Serializer):
    pass