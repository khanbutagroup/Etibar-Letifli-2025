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