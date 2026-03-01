from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from info.models import *
from info.forms import *


def quest_views(request):
    questions = Questions.objects.prefetch_related('answers').all()

    context = {
        'questions': questions,
    }

    return render(request, 'info/faq.html', context)


def contact_views(request):
    if request.method == 'POST':
        form = CotnactForm(request.POST)
        if form.is_valid():
            form.save()
            form = CotnactForm()

    else:
        form = CotnactForm()

    
    context = {
        'form': form,
    }
    return render(request, 'info/contact.html')


def about_views(request):
    about = About.objects.last()
    statistic = Statistic.objects.all()
    about_two = AboutTwo.objects.prefetch_related('about').all()

    context = {
        'about': about,
        'statistic': statistic,
        'about_two': about_two,
    }
    return render(request, 'info/about.html', context)



def pdf_views(request):
    pdf = PDF.objects.filter(is_active=True)

    context = {
        'pdf': pdf
    }
    return render(request, 'info/pdf.html', context)





def subscribe_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            Subscribe.objects.get_or_create(email=email)
            messages.success(request,  _("Təşəkkürlər, abonə oldunuz!"))
        else:
            messages.error(request, _("Email daxil edin."))
    return redirect(request.META.get('HTTP_REFERER', '/'))














from django.db.models import Q
from django.shortcuts import render
from info.models import *
from main.models import *
from exam.models import *
from video.models import *
from user.models import *

def global_search(request):
    query = request.GET.get("q", "").strip()
    results = {}

    if query:
        # 🧠 İmtahanlar
        exam_results = Exam.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        )

        # 📚 Kitablar
        book_results = Book.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )

        # 📄 PDF-lər
        pdf_results = PDF.objects.filter(
            Q(title__icontains=query) | Q(title_2__icontains=query),
            is_active=True
        )

        # 📰 Xəbərlər
        news_results = News.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )

        # ℹ️ Haqqımızda bölməsi
        about_results = About.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        # 📂 Kateqoriyalar (bütün səviyyələr)
        category_results = Category.objects.filter(title__icontains=query)
        subcategory_results = SubCategory.objects.filter(title__icontains=query)
        subsubcategory_results = SubSubCategory.objects.filter(title__icontains=query)
        subsubsubcategory_results = SubSubSubCategory.objects.filter(title__icontains=query)

        # Bütün nəticələri dictionary şəklində birləşdir
        results = {
            "exam": exam_results,
            "book": book_results,
            "pdf": pdf_results,
            "news": news_results,
            "about": about_results,
            "category": category_results,
            "subcategory": subcategory_results,
            "subsubcategory": subsubcategory_results,
            "subsubsubcategory": subsubsubcategory_results,
        }

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "info/searchResult.html", context)


def book_free_views(request):
    category_id = request.GET.get('category')

    book_free = BookFree.objects.select_related('category').order_by('-created_at')

    if category_id:
        book_free = book_free.filter(category_id=category_id)

    categories = BookFreeCategory.objects.all()

    # Seçilmiş kateqoriya obyekti
    active_category_obj = None
    if category_id:
        try:
            active_category_obj = categories.get(id=category_id)
        except BookFreeCategory.DoesNotExist:
            active_category_obj = None

    context = {
        'book_free': book_free,
        'categories': categories,
        'active_category': active_category_obj,  # artıq obyekt göndəririk
    }
    return render(request, 'info/book_free.html', context)


def test_views(request):
    category_id = request.GET.get('category')

    test = Test.objects.select_related('category').order_by('-created_at')

    if category_id:
        test = test.filter(category_id=category_id)

    categories = TestCategory.objects.all()

    active_category = None
    if category_id:
        active_category = categories.filter(id=category_id).first()

    context = {
        'test': test,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'info/test.html', context)


def expanation_views(request):
    category_id = request.GET.get('category')

    expanation = Expanation.objects.select_related('category').order_by('-created_at')

    if category_id:
        expanation = expanation.filter(category_id=category_id)

    categories = ExpanationCategory.objects.all()

    active_category = None
    if category_id:
        active_category = categories.filter(id=category_id).first()

    context = {
        'expanation': expanation,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'info/expanation.html', context)