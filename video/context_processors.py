from video.models import *

def video_context_processors(request):
    categories = VideoCategory.objects.all()

    return {
        'categories': categories,
    }