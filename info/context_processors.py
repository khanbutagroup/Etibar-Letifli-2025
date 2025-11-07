from info.models import *

def info_context_processors(request):
    contact = Contact.objects.last()
    sosial = SosialAccount.objects.last()
    about = About.objects.last()
    statistic = Statistic.objects.all()
    about_two = AboutTwo.objects.prefetch_related('about').all()
    logo = LogoFavicon.objects.last()
    
    return {
        'contact': contact,
        'sosial': sosial,
        'about': about,
        'statistic': statistic,
        'about_two': about_two,
        'logo': logo,
    }