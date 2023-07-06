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
    
    model_serializer = AnimeListSerializer

    def get(self, request):

        animes = Anime.objects.all()
        serializer = self.model_serializer(animes, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


