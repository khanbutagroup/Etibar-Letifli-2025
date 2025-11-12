from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q

from main.models import *
from main.forms import *
from exam.models import *

def news_views(request):

    news = News.objects.filter(is_active=True)
    paginator = Paginator(news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'news': news,
        'page_obj': page_obj,
    }
    return render(request, 'main/news.html', context)


def news_details(request, id):
    query = request.GET.get('search')


    if query:

        try:
            found_news = News.objects.filter(is_active=True, title__icontains=query).first()
            if found_news:
                return redirect('news_details', id=found_news.id)
        except News.DoesNotExist:
            pass  

    news = get_object_or_404(News, id=id, is_active=True)
    news_all = News.objects.filter(is_active=True).exclude(id=id).order_by('-created_at')[:6]

    context = {
        'news': news,
        'news_all': news_all,
        'search_query': query,
    }
    return render(request, 'main/news-details.html', context)


from django.shortcuts import render
from .models import Book, BookCategory, BookSubCategory

def book_views(request):
    book_category = BookCategory.objects.all()
    book_sub_category = BookSubCategory.objects.all()
    book = Book.objects.filter(is_active=True)

    # --- Axtarış üzrə filter (adı ilə)
    search_query = request.GET.get('search_name')
    if search_query:
        book = book.filter(title__icontains=search_query)

    # --- Qiymət aralığı filteri
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        book = book.filter(price__gte=min_price)
    if max_price:
        book = book.filter(price__lte=max_price)

    # --- Kateqoriya / sub-kateqoriya filteri
    category_id = request.GET.get('category')
    if category_id:
        # yalnız həmin kateqoriyaya aid sub-category-lər
        book_sub_category = book_sub_category.filter(category_id=category_id)
        # həmçinin kitabları filterləyə bilərik
        book = book.filter(category_id=category_id)

    # --- Sub-category filter
    sub_category_id = request.GET.get('sub_category')
    if sub_category_id:
        book = book.filter(sub_category_id=sub_category_id)

    # --- Sıralama (sort)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_asc':
        book = book.order_by('title')
    elif sort_by == 'name_desc':
        book = book.order_by('-title')
    elif sort_by == 'price_asc':
        book = book.order_by('price')
    elif sort_by == 'price_desc':
        book = book.order_by('-price')
    elif sort_by == 'latest':
        book = book.order_by('-created_at')

    context = {
        'book': book,
        'book_category': book_category,
        'book_sub_category': book_sub_category,
        'search_name': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'category_selected': category_id,
        'sub_category_selected': sub_category_id,
        'sort_selected': sort_by,
    }
    return render(request, 'main/books.html', context)



def book_details(request, id):

    book = get_object_or_404(Book, id=id, is_active=True)
    

    book.views_count += 1
    book.save(update_fields=['views_count'])
    


    context = {
        'book': book,

    }
    return render(request, 'main/book-details.html', context)



def index_views(request):
    index_slider = IndexSlider.objects.last()
    index_books = IndexBooks.objects.all()
    index_pdf = IndexPDFBooks.objects.all()
    news = News.objects.all().order_by('-created_at')
    exam = Exam.objects.filter(is_main=True)

    context = {
        'index_slider': index_slider,
        'index_books': index_books,
        'index_pdf': index_pdf,
        'news': news,
        'exam': exam,
    }
    return render(request, 'main/index.html', context)