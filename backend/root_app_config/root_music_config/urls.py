# django imports
from django.urls import path


# project view applications
from .views import (
    MusicCreateAPIView,
    MusicUpdateDeleteAndGetAPIView
)


urlpatterns = [
    path('', MusicCreateAPIView.as_view(), name='create_music'),
    path('<str:id>/', MusicCreateAPIView.as_view(), name="update-delete-and-get-music")
    
]