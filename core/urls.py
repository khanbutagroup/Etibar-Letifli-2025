# """
# URL configuration for core project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns 



# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path('', include('main.urls')),
#     path('info/', include('info.urls')),
#     path('user/', include('user.urls')),
#     path('video/', include('video.urls')),
#     path('exam/', include('exam.urls')),


#     path('rosetta/', include('rosetta.urls')),
#     path('ckeditor/', include('ckeditor_uploader.urls')),


# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from main.views import set_language
from django.shortcuts import redirect


def root_redirect(request):
    return redirect('/az/')


urlpatterns = [
    path('', root_redirect),  # / → /az/
    path('admin/', admin.site.urls),
    path('set-language/<str:language>/', set_language, name='set_language'),

    path('rosetta/', include('rosetta.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('info/', include('info.urls')),
    path('user/', include('user.urls')),
    path('video/', include('video.urls')),
    path('exam/', include('exam.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
