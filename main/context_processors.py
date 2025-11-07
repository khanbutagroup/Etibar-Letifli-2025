from main.models import BookCategory, BookSubCategory

def categories(request):
    categories = BookCategory.objects.all()
    sub_categories = BookSubCategory.objects.all()
    category_selected = request.GET.get('category', '')  # GET parametri varsa al, yoxsa ''
    return {
        'book_category': categories,
        'book_sub_category': sub_categories,
        'category_selected': category_selected,
    }