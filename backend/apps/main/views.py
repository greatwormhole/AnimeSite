from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .serializers import *
from .models import Anime, Manga

class ContentListView(APIView):

    serializer_class = None
    model_class = None

    def get(self, request):

        objects = self.model_class.objects.all()
        serializer = self.serializer_class(objects, many=True)
        response = Response(serializer.data, status=HTTP_200_OK)

        return response
    
class ContentDetailView(APIView):

    serializer_class = None
    model_class = None

    def get(self, request, pk):

        try:
            obj = self.model_class.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'error': "Object doesn't exist"}, status=HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(obj)
        response = Response(serializer.data, status=HTTP_200_OK)

        return response

class AnimeListView(ContentListView):
    
    serializer_class = AnimeListSerializer
    model_class = Anime

class AnimeDetailView(ContentDetailView):

    serializer_class = AnimeDetailSerializer
    model_class = Anime

class MangaListView(ContentListView):

    serializer_class = MangaListSerializer
    model_class = Manga
    
class MangaDetailView(ContentDetailView):

    serializer_class = MangaDetailSerializer
    model_class = Manga