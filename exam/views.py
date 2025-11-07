from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
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
def take_exam(request, exam_id, page=1):
    exam = get_object_or_404(Exam, pk=exam_id)
    purchased_exam = get_object_or_404(PurchasedExam, user=request.user, exam=exam)

    now = timezone.now()

    # İmtahan hələ başlamayıb və ya bitibsə
    if exam.start_date and now < exam.start_date:
        return HttpResponse(f"İmtahan {exam.start_date.strftime('%d.%m.%Y %H:%M')} tarixində başlayacaq.")
    if purchased_exam.finished_at and now > purchased_exam.finished_at:
        return HttpResponse("İmtahan müddəti bitib!")

    questions = exam.questions_answers.all().order_by('id')
    per_page = 1
    start = (page - 1) * per_page
    end = start + per_page
    question = questions[start:end].first()

    session, _ = UserExamSession.objects.get_or_create(user=request.user, exam=exam, finished_at=None)

    if request.method == "POST":
        selected_option = request.POST.get(f"question_{question.id}")
        if selected_option:
            UserAnswer.objects.update_or_create(
                session=session,
                question=question,
                defaults={"selected_option": selected_option}
            )
        if end >= len(questions) or (purchased_exam.finished_at and timezone.now() >= purchased_exam.finished_at):
            session.finished_at = timezone.now()
            session.save()
            return redirect("exam_finish", session_id=session.id)
        return redirect("take_exam", exam_id=exam.id, page=page+1)

    # qalan vaxtı saniyə ilə hesabla
    if purchased_exam.finished_at:
        total_seconds = int((purchased_exam.finished_at - now).total_seconds())
    else:
        total_seconds = (exam.duration_minutes or 60) * 60

    return render(request, "exam/startExam.html", {
        "exam": exam,
        "question": question,
        "page": page,
        "total": len(questions),
        "session": session,
        "total_seconds": total_seconds
    })


@login_required
def finish_exam(request, session_id):
    session = get_object_or_404(UserExamSession, id=session_id)
    if not session.finished_at:
        session.finished_at = timezone.now()
        session.save()

    total_points = 0
    for ua in session.answers.all():
        q = ua.question
        selected_field = f'is_correct_{ua.selected_option.lower()}'
        if getattr(q, selected_field):
            total_points += q.points

    return render(request, "exam/result.html", {
        "session": session,
        "total_points": total_points,
    })
