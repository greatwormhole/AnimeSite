from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Anime, Manga

class ContentListSerializer(ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'created', 'image']

class ContentDetailSerializer(ModelSerializer):

    rating = SerializerMethodField('content_rating')
    
    def content_rating(self, content):
        return round(content.rating, 2)
    
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

    class Meta(ContentDetailSerializer.Meta):
        model = Anime

class MangaDetailSerializer(ContentDetailSerializer):

    class Meta(ContentDetailSerializer.Meta):
        model = Manga