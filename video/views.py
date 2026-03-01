from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from video.models import *
from info.models import *
from django.urls import reverse


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





import uuid
import requests
from django.conf import settings
from exam.views import kb_headers   # mövcud header funksiyası
from video.models import VideoPayment


@login_required
def buy_video(request, video_id):

    video = get_object_or_404(Video, id=video_id, is_active=True)

    # artıq alıbsa yenidən aldırmayaq
    if PurchasedVideo.objects.filter(user=request.user, video=video).exists():
        messages.info(request, "Bu videonu artıq almısınız.")
        return redirect("account")

    order_id = str(uuid.uuid4())

    payment = VideoPayment.objects.create(
        user=request.user,
        video=video,
        order_id=order_id,
        amount=video.price
    )

    url = f"{settings.KB_BASE_URL}/order"

    payload = {
        "order": {
            "typeRid": "Order_SMS",
            "amount": str(float(video.price)),
            "currency": "AZN",
            "language": "az",
            "description": video.title,
            "hppRedirectUrl": request.build_absolute_uri(
                reverse("video_payment_result")
            )
        }
    }

    response = requests.post(url, json=payload, headers=kb_headers())

    if response.status_code != 200:
        payment.status = "FAILED"
        payment.save()
        messages.error(request, "Bankla əlaqə xətası.")
        return redirect("video_detail", video_id=video.id)

    data = response.json()["order"]

    payment.kb_order_id = data["id"]
    payment.kb_password = data["password"]
    payment.save()

    redirect_url = f"{data['hppUrl']}?id={data['id']}&password={data['password']}"

    return redirect(redirect_url)


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    context = {
        'video': video
    }
    return render(request, 'video/info-video.html', context)





@login_required
def video_payment_result(request):

    kb_order_id = request.GET.get("ID")

    payment = VideoPayment.objects.filter(kb_order_id=kb_order_id).first()

    if not payment:
        messages.error(request, "Ödəniş tapılmadı.")
        return redirect("video")

    verify_url = f"{settings.KB_BASE_URL}/order/{kb_order_id}"
    verify_response = requests.get(verify_url, headers=kb_headers())
    verify_json = verify_response.json()

    if "order" not in verify_json:
        messages.error(request, "Bank cavabında xəta var.")
        return redirect("video")

    real_status = verify_json["order"]["status"]

    if real_status == "FullyPaid":

        payment.status = "SUCCESS"
        payment.save()

        # Aktivlik müddətini hesablayırıq
        expires_at = timezone.now() + timedelta(days=payment.video.active_period_days)

        PurchasedVideo.objects.get_or_create(
            user=payment.user,
            video=payment.video,
            defaults={"expires_at": expires_at}
        )

        messages.success(request, "Video uğurla alındı ✅")

    else:
        payment.status = "FAILED"
        payment.save()
        messages.error(request, "Ödəniş uğursuz oldu ❌")

    return redirect("account")