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