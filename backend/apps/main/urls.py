from django.urls import path
from .views import *

urlpatterns = [
    path('animes/', AnimeListView.as_view(), name='anime_list'),
    path('mangas/', MangaListView.as_view(), name='manga_list'),
    path('animes/<int:pk>/', AnimeDetailView.as_view(), name='detail_anime'),
    path('mangas/<int:pk>/', MangaDetailView.as_view(), name='detail_manga'),
]
