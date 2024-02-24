# django imports
from django.urls import path


# project view applications
from .views import (
    MusicCreateAPIView,
    MusicUpdateDeleteAndGetAPIView,
    get_media_path,
)


urlpatterns = [
    path('', MusicCreateAPIView.as_view(), name='create_music'),
    path('<str:id>/', MusicUpdateDeleteAndGetAPIView.as_view(), name="update-delete-and-get-music"),
    path("media/<str:path>", get_media_path, name="get-media-path"),
]