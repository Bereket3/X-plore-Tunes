from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/' , include("drf_social_oauth2.urls", namespace='drf')),
    path('api_root/auth/', include('root_user.urls')),
    path('api_root/music/', include('root_music_config.urls'))
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]