from django.urls import path
from info.views import *


urlpatterns = [
    path('faq/', quest_views, name='faq'),
    path('contact/', contact_views, name='contact'),
    path('about/', about_views, name='about'),
    path('pdf/', pdf_views, name='pdf'),
    path('subscribe/', subscribe_view, name='subscribe'),
]