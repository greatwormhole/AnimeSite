from rest_framework.routers import DefaultRouter

from .views import *

main_router = DefaultRouter()
main_router.register(r'animes', AnimeViewSet)
main_router.register(r'mangas', MangaViewSet)

urlpatterns = [
    
]

urlpatterns += main_router.urls