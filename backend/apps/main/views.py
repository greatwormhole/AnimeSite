from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *

class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    
    def get_permissions(self):
        match self.action:
            case 'list':
                permission_classes = [AllowAny]
            case 'retrieve':
                permission_classes = [AllowAny]
            case _:
                permission_classes = [DjangoModelPermissions]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return AnimeListSerializer
            case _:
                return AnimeDetailSerializer

class MangaViewSet(ModelViewSet):
    queryset = Manga.objects.all()
        
    def get_permissions(self):
        match self.action:
            case 'list':
                permission_classes = [AllowAny]
            case 'retrieve':
                permission_classes = [AllowAny]
            case _:
                permission_classes = [DjangoModelPermissions]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        match self.action:
            case 'list':    
                return MangaListSerializer
            case _:
                return MangaDetailSerializer

class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    
    def get_permissions(self):
        match self.action:
            case 'list':
                pass
            case '':
                pass