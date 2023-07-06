from rest_framework.serializers import ModelSerializer
from .models import Anime

class AnimeListSerializer(ModelSerializer):

    class Meta:
        model = Anime