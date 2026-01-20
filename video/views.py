from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from video.models import *
from info.models import *


def video_views(request):
    courses = Course.objects.filter(content_type='video')

    category_id = request.GET.get('category')
    sub_category_id = request.GET.get('subcategory')

    videos = Video.objects.filter(is_active=True)

    if category_id:
        videos = videos.filter(category_id=category_id)

    if sub_category_id:
        videos = videos.filter(sub_category_id=sub_category_id)

    categories = VideoCategory.objects.prefetch_related('videosubcategory_set').all()

    context = {
        'videos': videos,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_subcategory': int(sub_category_id) if sub_category_id else None,
        'courses': courses,
    }
    return render(request, 'video/videoLessons.html', context)




def video_info_view(request, video_id):
    # Hansi videodan kliklendiyini tapırıq
    video = get_object_or_404(Video, id=video_id, is_active=True)

    context = {
        'video': video
    }
    return render(request, 'video/info-video.html', context)


def free_video_views(request):
    free_video = FreeVideo.objects.filter(is_active=True)

    context = {
        'free_video': free_video,
    }
    return render(request, 'video/videoLessonsFree.html', context)





@login_required
def buy_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    purchased_video, created = PurchasedVideo.objects.get_or_create(
        user=request.user,
        video=video,
    )
    if created:
        # Videonun aktivlik müddətini hesabla
        purchased_video.expires_at = timezone.now() + timedelta(days=video.active_period_days)
        purchased_video.save()

    return redirect('account')


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    context = {
        'video': video
    }
    return render(request, 'video/info-video.html', context)