from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_video, name='download_video'),
    path('get_video_formats/', views.get_video_formats, name='get_video_formats'),
]
