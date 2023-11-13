from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import *

accounts_router = DefaultRouter()
accounts_router.register(r'', UserViewSet)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh/', RefreshJWTTokenView.as_view(), name='refresh_JWT'),
]

urlpatterns += accounts_router.urls