from video.models import *

def video_context_processors(request):
    """
    Bütün templates üçün VideoCategory-lər və subcategory-lər.
    """
    categories = VideoCategory.objects.prefetch_related('videosubcategory_set').all()

    return {
        'categories': categories,  # video sidebar üçün
    }