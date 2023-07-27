from rest_framework.serializers import ModelSerializer
from .models import Anime, Manga

class ContentListSerializer(ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'created', 'image', 'rating']

class ContentDetailSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        depth = 1

class AnimeListSerializer(ContentListSerializer):

    class Meta(ContentListSerializer.Meta):
        model = Anime

class MangaListSerializer(ContentListSerializer):

    class Meta(ContentListSerializer.Meta):
        model = Manga

class AnimeDetailSerializer(ContentDetailSerializer):

    class Meta(ContentListSerializer.Meta):
        model = Anime

class MangaDetailSerializer(ContentDetailSerializer):

    class Meta(ContentListSerializer.Meta):
        model = Manga