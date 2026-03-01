import uuid
import requests
import hmac
import hashlib
import base64
import json




from django.urls import reverse

from exam.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404


def exam_list(request):
    
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    subsubcategory_id = request.GET.get('subsubcategory')
    subsubsubcategory_id = request.GET.get('subsubsubcategory')

    all_categories = Category.objects.prefetch_related(
        'subcategory_set__subsubcategory_set__subsubsubcategory_set'
    ).all()

    active_title = "Bütün kateqoriyalar"
    categories = None
    subcategories = None
    subsubcategories = None
    subsubsubcategories = None
    exams = None


    category = None
    subcategory = None
    subsubcategory = None
    subsubsubcategory = None


    # 1️⃣ Əsas səviyyə - Kateqoriyalar
    if not category_id:
        categories = all_categories

    # 2️⃣ Alt səviyyə - SubCategory-lər
    elif category_id and not subcategory_id:
        category = get_object_or_404(Category, id=category_id)
        active_title = category.title
        subcategories = category.subcategory_set.all()

    # 3️⃣ Daha alt səviyyə - SubSubCategory-lər
    elif subcategory_id and not subsubcategory_id:
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        active_title = subcategory.title
        subsubcategories = subcategory.subsubcategory_set.all()

    # 4️⃣ Ən alt səviyyə - SubSubSubCategory-lər
    elif subsubcategory_id and not subsubsubcategory_id:
        subsubcategory = get_object_or_404(SubSubCategory, id=subsubcategory_id)
        active_title = subsubcategory.title
        subsubsubcategories = subsubcategory.subsubsubcategory_set.all()

    # 5️⃣ Ən dərin səviyyə - artıq imtahanları göstər
    elif subsubsubcategory_id:
        subsubsubcategory = get_object_or_404(SubSubSubCategory, id=subsubsubcategory_id)
        active_title = subsubsubcategory.title
        exams = Exam.objects.filter(sub_sub_sub_category=subsubsubcategory).order_by('title')

    return render(request, "exam/exams.html", {
        "categories": categories,
        "subcategories": subcategories,
        "subsubcategories": subsubcategories,
        "subsubsubcategories": subsubsubcategories,
        "exams": exams,
        "active_title": active_title,
        "all_categories": all_categories,
        'selected_category': category if category_id else None,
        'selected_subcategory': subcategory if subcategory_id else None,
        'selected_subsubcategory': subsubcategory if subsubcategory_id else None,
        'selected_subsubsubcategory': subsubsubcategory if subsubsubcategory_id else None,

    })

import base64

def kb_headers():
    credentials = f"{settings.KB_USERNAME}:{settings.KB_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()

    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }



@login_required
def buy_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if not exam.price:
        return HttpResponse("Qiymət təyin edilməyib")

    order_id = str(uuid.uuid4())

    payment = Payment.objects.create(
        user=request.user,
        exam=exam,
        order_id=order_id,
        amount=exam.price
    )

    url = f"{settings.KB_BASE_URL}/order"

    payload = {
        "order": {
            "typeRid": "Order_SMS",
            "amount": str(float(exam.price)),  # string göndər
            "currency": "AZN",
            "language": "az",
            "description": exam.title,
            "hppRedirectUrl": request.build_absolute_uri(
                reverse("payment_result")
            )
        }
    }

    response = requests.post(url, json=payload, headers=kb_headers())

    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        payment.status = "FAILED"
        payment.save()
        return HttpResponse(response.text)

    data = response.json()["order"]

    hpp_url = data["hppUrl"]
    kb_order_id = data["id"]
    kb_password = data["password"]

    payment.kb_order_id = kb_order_id
    payment.kb_password = kb_password
    payment.save()

    redirect_url = f"{hpp_url}?id={kb_order_id}&password={kb_password}"
    print("REDIRECT:", redirect_url)
    return redirect(redirect_url)











# @login_required
# def buy_exam(request, exam_id):
#     exam = get_object_or_404(Exam, id=exam_id)

#     if not exam.price:
#         return HttpResponse("Qiymət təyin edilməyib")

#     order_id = str(uuid.uuid4())
#     idempotency_key = str(uuid.uuid4())

#     payment = Payment.objects.create(
#         user=request.user,
#         exam=exam,
#         order_id=order_id,
#         amount=exam.price
#     )

#     token = get_birpay_token()

#     url = f"{settings.BIRPAY_BASE_URL}/v1/payments"

#     payload = {
#         "amount": str(exam.price),
#         "currency": "AZN",
#         "description": f"{exam.title} imtahanı",
#         "orderId": order_id,

#         "confirmation": {
#             "type": "REDIRECT",
#             "returnUrl": request.build_absolute_uri("/payment/result/")
#         },

#         "callbackUrl": request.build_absolute_uri("/payment/webhook/"),

#         "posDetail": {
#             "merchantId": settings.BIRPAY_MERCHANT_ID,
#             "terminalId": settings.BIRPAY_TERMINAL_ID
#         }
#     }

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}",
#         "X-Idempotency-Key": idempotency_key
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print(response.status_code)
#     print(response.text)

#     if response.status_code in [200, 201]:
#         data = response.json()
#         confirmation_url = data["confirmation"]["confirmationUrl"]
#         return redirect(confirmation_url)

#     payment.status = "FAILED"
#     payment.save()

#     return HttpResponse(f"Birpay Xəta: {response.text}")






@csrf_exempt
def payment_callback(request):
    order_id = request.GET.get("orderId")
    status = request.GET.get("status")

    payment = get_object_or_404(Payment, order_id=order_id)

    if status == "SUCCESS":
        payment.status = "SUCCESS"
        payment.save()

        PurchasedExam.objects.get_or_create(
            user=payment.user,
            exam=payment.exam
        )

        return HttpResponse("OK")

    payment.status = "FAILED"
    payment.save()

    return HttpResponse("FAILED")




def verify_signature(payload, received_signature):
    secret = settings.BIRPAY_WEBHOOK_SECRET.encode()

    computed_hmac = hmac.new(
        secret,
        payload,
        hashlib.sha256
    ).digest()

    generated_signature = base64.b64encode(computed_hmac).decode()

    return hmac.compare_digest(generated_signature, received_signature)










@csrf_exempt
def birpay_webhook(request):
    payload = request.body
    signature = request.headers.get("X-Signature")

    if not signature:
        return HttpResponse("Missing signature", status=400)

    if not verify_signature(payload, signature):
        return HttpResponse("Invalid signature", status=400)

    data = json.loads(payload)

    event = data.get("event")
    payment_data = data.get("payload", {})
    order_id = payment_data.get("orderId")
    status = payment_data.get("status")

    payment = Payment.objects.filter(order_id=order_id).first()

    if not payment:
        return HttpResponse("Payment not found", status=404)

    if event == "payment_succeeded":
        payment.status = "SUCCESS"
        payment.save()

        PurchasedExam.objects.get_or_create(
            user=payment.user,
            exam=payment.exam
        )

    elif event in ["payment_canceled", "payment_failed"]:
        payment.status = "FAILED"
        payment.save()

    return HttpResponse("OK")






@login_required
def start_exam(request, exam_id):
    purchased_exam = get_object_or_404(
        PurchasedExam,
        user=request.user,
        exam_id=exam_id
    )
    exam = purchased_exam.exam
    now = timezone.now()

    # ❌ ƏGƏR İMTAHANA ARTİQ GİRİBSƏ
    if purchased_exam.started_at:
        return HttpResponse(
            "Bu imtahana artıq daxil olmusunuz. Yenidən giriş mümkün deyil."
        )

    # İmtahan hələ başlamayıb
    if exam.start_date and now < exam.start_date:
        return HttpResponse(
            f"İmtahan {exam.start_date.strftime('%d.%m.%Y %H:%M')} tarixində başlayacaq."
        )

    # İmtahan bitib
    if exam.end_date and now > exam.end_date:
        return HttpResponse("İmtahan artıq bitib.")

    # ✅ İLK VƏ YEGANƏ DAXİL OLMA ANI
    purchased_exam.started_at = now

    if exam.duration_minutes:
        purchased_exam.finished_at = now + timezone.timedelta(
            minutes=exam.duration_minutes
        )

    purchased_exam.save()

    return redirect('take_exam_first', exam_id=exam.id)


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    purchased_exam = get_object_or_404(PurchasedExam, user=request.user, exam=exam)
    now = timezone.now()



    # ❌ Heç başlamayıbsa buraya düşməsin
    if not purchased_exam.started_at:
        return redirect('exam_list')

    # ❌ Vaxt bitibsə
    if purchased_exam.finished_at and timezone.now() > purchased_exam.finished_at:
        return HttpResponse("İmtahan müddəti bitib.")

    # imtahan vaxtı yoxlamaları
    if exam.start_date and now < exam.start_date:
        return HttpResponse(f"İmtahan {exam.start_date.strftime('%d.%m.%Y %H:%M')} tarixində başlayacaq.")
    if purchased_exam.finished_at and now > purchased_exam.finished_at:
        return HttpResponse("İmtahan müddəti bitib!")

    session, _ = UserExamSession.objects.get_or_create(user=request.user, exam=exam, finished_at=None)

    # === POST zamanı bütün cavabları qəbul et ===
    if request.method == "POST":
        for question in exam.questions_answers.all():
            selected_option = request.POST.get(f"question_{question.id}")
            if selected_option:
                UserAnswer.objects.update_or_create(
                    session=session,
                    question=question,
                    defaults={"selected_option": selected_option}
                )

        # istifadəçi "imtahanı bitir" düyməsinə basıbsa
        if "finishExam" in request.POST:
            session.finished_at = timezone.now()
            session.save()
            return redirect("exam_finish", session_id=session.id)

    # qalan vaxt
    total_seconds = 0
    if purchased_exam.finished_at:
        total_seconds = int((purchased_exam.finished_at - now).total_seconds())

    return render(request, "exam/startExam.html", {
        "exam": exam,
        "session": session,
        "total_seconds": total_seconds,
    })



@login_required
def finish_exam(request, session_id):
    session = get_object_or_404(UserExamSession, id=session_id, user=request.user)
    request.session['last_session_id'] = session.id
    exam = session.exam
    now = timezone.now()

    forced_finish = False
    if not session.finished_at:
        session.finished_at = now
        session.save()
        forced_finish = True 

    # Bitmə vaxtı qeyd et
    if not session.finished_at:
        session.finished_at = timezone.now()
        session.save()

    answers = session.answers.select_related("question")
    total_questions = exam.questions_answers.count()

    correct_count = 0
    wrong_count = 0

    for ua in answers:
        q = ua.question
        selected_opt = ua.selected_option
        if not selected_opt:
            continue

        selected_field = f'is_correct_{selected_opt.lower()}'
        is_correct = getattr(q, selected_field, False)
        ua.is_correct = is_correct

        if is_correct:
            correct_count += 1
        else:
            wrong_count += 1

    unanswered_count = total_questions - (correct_count + wrong_count)

    # ✅ modeldəki məntiqi burda işə sal
    exam.right_number = correct_count
    exam.row_number = wrong_count

    final_points = exam.logical_calculation()
    session.final_points = final_points
    session.save()
    context = {
        "session": session,
        "exam": exam,
        "answers": answers,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "unanswered_count": unanswered_count,
        "total_questions": total_questions,
        "final_points": final_points,
        "calculation_type": exam.get_calculation_types_display(),
    }

    return render(request, "exam/result.html", context)







@login_required
def exam_review(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # İstifadəçi imtahanı bitiribmi?
    session = (
        UserExamSession.objects
        .filter(user=request.user, exam=exam, finished_at__isnull=False)
        .order_by('-finished_at')
        .first()
    )

    if not session:
        messages.error(request, "Bu imtahan üçün rəy yazmaq üçün əvvəlcə imtahanı bitirməlisiniz.")
        return redirect('exam_list')

    # POST (rəy göndərilibsə)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()

        # eyni imtahan üçün eyni user təkrar rəy yaza bilməsin
        if ExamReview.objects.filter(user=request.user, exam=exam).exists():
            messages.warning(request, "Bu imtahan üçün artıq rəy yazmısınız.")
            return redirect('exam_finish', session_id=session.id)

        ExamReview.objects.create(
            user=request.user,
            exam=exam,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Rəyiniz uğurla göndərildi. Təşəkkürlər!")
        return redirect('exam_finish', session_id=session.id)

    # GET (formun açılması)
    return render(request, 'main/writeComments.html', {'exam': exam})




from django.db.models import Avg, Count


def exam_comments(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    comments = exam.reviews.select_related('user')

    # Rəylərin statistikası
    stats = exam.reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    # Hər səviyyəyə görə say
    rating_counts = exam.reviews.values('rating').annotate(count=Count('id')).order_by('-rating')

    # 1-dən 5-ə qədər sıralama üçün sıfır olanlar da əlavə olunsun
    rating_distribution = {i: 0 for i in range(1, 6)}
    for item in rating_counts:
        rating_distribution[item['rating']] = item['count']

    context = {
        'exam': exam,
        'comments': comments,
        'avg_rating': round(stats['avg_rating'] or 0, 1),
        'total_reviews': stats['total_reviews'] or 0,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'main/comments.html', context)


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    context = {
        'exam': exam
    }
    return render(request, 'exam/info-exam.html', context)


from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

@login_required
def payment_result(request):
    kb_order_id = request.GET.get("ID")

    payment = Payment.objects.filter(kb_order_id=kb_order_id).first()

    if not payment:
        messages.error(request, "Ödəniş tapılmadı.")
        return redirect("exam_list")

    verify_url = f"{settings.KB_BASE_URL}/order/{kb_order_id}"
    verify_response = requests.get(verify_url, headers=kb_headers())
    verify_json = verify_response.json()

    if "order" not in verify_json:
        messages.error(request, "Bank cavabında xəta var.")
        return redirect("exam_list")

    real_status = verify_json["order"]["status"]

    if real_status == "FullyPaid":
        payment.status = "SUCCESS"
        payment.save()

        PurchasedExam.objects.get_or_create(
            user=payment.user,
            exam=payment.exam
        )

        messages.success(request, "Ödəniş uğurla tamamlandı ✅")

    else:
        payment.status = "FAILED"
        payment.save()
        messages.error(request, "Ödəniş uğursuz oldu ❌")

    return redirect("index")

def get_birpay_token():
    url = f"{settings.BIRPAY_BASE_URL}/oauth/token"

    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(settings.BIRPAY_CLIENT_ID, settings.BIRPAY_CLIENT_SECRET),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code != 200:
        raise Exception(f"Token error: {response.text}")

    return response.json()["access_token"]