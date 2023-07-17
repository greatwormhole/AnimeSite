from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAdminUser
from .models import AuthUser
from .serializers import UserSerializer

class UserListView(APIView):

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def get(self, request):

        users = AuthUser.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response(serializer.data, status=HTTP_200_OK)