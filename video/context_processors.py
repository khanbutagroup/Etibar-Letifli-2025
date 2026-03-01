from video.models import *

def video_context_processors(request):
    """
    Bütün templates üçün VideoCategory-lər və subcategory-lər.
    """
    categoriess = VideoCategory.objects.prefetch_related('videosubcategory_set').all()

    return {
        'categoriess': categoriess,  # video sidebar üçün
    }



