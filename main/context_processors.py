from main.models import BookCategory, BookSubCategory, MetaTags

def categories(request):
    categories = BookCategory.objects.all()
    sub_categories = BookSubCategory.objects.all()
    category_selected = request.GET.get('category', '')  # GET parametri varsa al, yoxsa ''
    return {
        'book_category': categories,
        'book_sub_category': sub_categories,
        'category_selected': category_selected,
    }


def meta_tags(request):
    path = request.resolver_match.url_name if request.resolver_match else "default"
    try:
        meta = MetaTags.objects.get(page=path)
    except MetaTags.DoesNotExist:
        meta = None

    return {
        "meta": meta
    }