from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from exam.models import *

def exam_list(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    subsubcategory_id = request.GET.get('subsubcategory')
    subsubsubcategory_id = request.GET.get('subsubsubcategory')

    exams = Exam.objects.select_related(
        'sub_sub_sub_category',
        'sub_sub_sub_category__sub_sub_category',
        'sub_sub_sub_category__sub_sub_category__sub_category',
        'sub_sub_sub_category__sub_sub_category__sub_category__category'
    )

    if subsubsubcategory_id:
        exams = exams.filter(sub_sub_sub_category_id=subsubsubcategory_id)
    elif subsubcategory_id:
        exams = exams.filter(sub_sub_sub_category__sub_sub_category_id=subsubcategory_id)
    elif subcategory_id:
        exams = exams.filter(sub_sub_sub_category__sub_sub_category__sub_category_id=subcategory_id)
    elif category_id:
        exams = exams.filter(sub_sub_sub_category__sub_sub_category__sub_category__category_id=category_id)

    exams = exams.order_by('title')

    categories = {}
    for exam in exams:
        cat = exam.sub_sub_sub_category.sub_sub_category.sub_category.category.title \
            if exam.sub_sub_sub_category and exam.sub_sub_sub_category.sub_sub_category and \
               exam.sub_sub_sub_category.sub_sub_category.sub_category and \
               exam.sub_sub_sub_category.sub_sub_category.sub_category.category else "Digər"
        subcat = exam.sub_sub_sub_category.sub_sub_category.title if exam.sub_sub_sub_category and exam.sub_sub_sub_category else "Digər"
        subsubcat = exam.sub_sub_sub_category.title if exam.sub_sub_sub_category else "Digər"
        categories.setdefault(cat, {}).setdefault(subcat, {}).setdefault(subsubcat, []).append(exam)

    all_categories = Category.objects.prefetch_related(
        'subcategory_set__subsubcategory_set__subsubsubcategory_set'
    ).all()

    return render(request, "exam/exams.html", {
        "categories": categories,
        "all_categories": all_categories,
        "exams": exams
    })


@login_required
def buy_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    PurchasedExam.objects.get_or_create(user=request.user, exam=exam)
    return redirect('account')





@login_required
def start_exam(request, exam_id):
    purchased_exam = get_object_or_404(PurchasedExam, user=request.user, exam_id=exam_id)
    exam = purchased_exam.exam

    now = timezone.now()

    # İmtahan hələ başlamayıb
    if exam.start_date and now < exam.start_date:
        return HttpResponse(f"İmtahan {exam.start_date.strftime('%d.%m.%Y %H:%M')} tarixində başlayacaq.")

    # İmtahan bitib
    if exam.end_date and now > exam.end_date:
        return HttpResponse("İmtahan artıq bitib.")

    # İstifadəçi imtahana başlayırsa, started_at və finished_at (timer) təyin olunur
    if not purchased_exam.started_at:
        purchased_exam.started_at = now
        if exam.duration_minutes:
            purchased_exam.finished_at = now + timezone.timedelta(minutes=exam.duration_minutes)
        purchased_exam.save()

    return redirect('take_exam_first', exam_id=exam.id)


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    purchased_exam = get_object_or_404(PurchasedExam, user=request.user, exam=exam)
    now = timezone.now()

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