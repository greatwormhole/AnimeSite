from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import AnimeListSerializer
from .models import Anime

class MainAPIView(APIView):
    
    def get(self, request):
        pass

class LoginAPIView(APIView):
    pass

class AnimeListView(APIView):
    
    serializer_class = AnimeListSerializer

    def get(self, request):

        animes = Anime.objects.all()
        serializer = self.serializer_class(animes, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


