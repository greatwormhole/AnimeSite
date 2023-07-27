from django.urls import path
from .views import *

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh/', RefreshJWTTokenView.as_view(), name='refresh_JWT'),
]