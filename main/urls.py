from django.urls import path
from main.views import *


urlpatterns = [
    path('news/', news_views, name='news'),
    path('news/<int:id>/', news_details, name='news_details'),
    path('book/', book_views, name='book'),
    path('book/<int:id>/', book_details, name='book_details'),
    path('', index_views, name='index'),
]