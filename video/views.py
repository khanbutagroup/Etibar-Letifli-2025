from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from video.models import *

def video_views(request, category_id=None, sub_category_id=None):
    videos = Video.objects.filter(is_active=True).select_related('category', 'sub_category')

    if category_id:
        videos = videos.filter(category_id=category_id)

    if sub_category_id:
        videos.filter(sub_category_id=sub_category_id)

    categories = VideoCategory.objects.all()

    context = {
        'videos': videos,
        'category_id': category_id,
        'sub_category_id': sub_category_id,
        'categories': categories,
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