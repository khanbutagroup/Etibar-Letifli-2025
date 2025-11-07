from django.urls import path
from video.views import *

urlpatterns = [
    path('videos/', video_views, name='video'),
    path('videos/category/<int:category_id>/', video_views, name='video_category'),
    path('videos/category/<int:category_id>/sub/<int:sub_category_id>/', video_views, name='video_subcategory'),
    path('video/<int:video_id>/info/', video_info_view, name='video_info'),
    path('free_video/', free_video_views, name='free_video'),
    path('buy-video/<int:video_id>/', buy_video, name='buy_video'),
]
