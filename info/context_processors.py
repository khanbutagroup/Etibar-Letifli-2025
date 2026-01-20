from info.models import *
from user.models import *


def info_context_processors(request):
    contact = Contact.objects.last()
    sosial = SosialAccount.objects.last()
    about = About.objects.last()
    statistic = Statistic.objects.all()
    about_two = AboutTwo.objects.prefetch_related('about').all()
    logo = LogoFavicon.objects.last()
    delivery = DeliveryPrice.objects.last()
    book_free_category = BookFreeCategory.objects.all()


    exam_course = Course.objects.filter(content_type='exam').first()
    exam_description = exam_course.description if exam_course else ''

    # Video description
    video_course = Course.objects.filter(content_type='video').first()
    video_description = video_course.description if video_course else ''


    return {
        'contact': contact,
        'sosial': sosial,
        'about': about,
        'statistic': statistic,
        'about_two': about_two,
        'logo': logo,
        'delivery': delivery,
        'course_exam_description': exam_description,
        'course_video_description': video_description,
        'book_free_category': book_free_category,
    }