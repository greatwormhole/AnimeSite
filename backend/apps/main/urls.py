from django.urls import path
from .views import AnimeListView

urlpatterns = [
    path('animes', AnimeListView.as_view(), name='anime_list')
]
