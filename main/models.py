from django.db import models
from ckeditor.fields import RichTextField
from info.models import *

class News(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    title = models.TextField(null=True, blank=True, verbose_name='Başlıq')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')
    created_at = models.DateField(auto_now_add=True, null=True, verbose_name='Yaradılma tarixi')
    is_active = models.BooleanField(default=True, null=True, verbose_name='Aktivdir?')

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, null=True, verbose_name='Meta Description')
    meta_keywords = models.TextField(blank=True, null=True, verbose_name='Meta Keywords')

    class Meta:
        verbose_name='Xəbərlər'
        verbose_name_plural='Xəbərlər'

# ≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠



class BookCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')

    class Meta:
        verbose_name = 'Kitab Kateqoriyası'
        verbose_name_plural = 'Kitab Kateqoriyaları'

    def __str__(self):
        return self.title or 'Kateqoriya'

class BookSubCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')

    class Meta:
        verbose_name = 'Kitab Sub Kateqoriyası'
        verbose_name_plural = 'Kitab Sub Kateqoriyaları'

    def __str__(self):
        return self.title or 'Sub Kateqoriya'

class Book(models.Model):
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kateqoriya')
    sub_category = models.ForeignKey(BookSubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Sub Kateqoriya')

    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Ad')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True, verbose_name='Qiymət')
    old_price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True, verbose_name='Köhnə Qiymət')
    ticket = models.CharField(max_length=128, null=True, blank=True, verbose_name='Etiket')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    sample_pages = models.FileField(upload_to='sample/', null=True, blank=True, verbose_name='Nümunə səhifələr')
    answers = models.FileField(upload_to='image/', null=True, blank=True, verbose_name='Cavablar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir?')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Baxış sayı')

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, null=True, verbose_name='Meta Description')
    meta_keywords = models.TextField(blank=True, null=True, verbose_name='Meta Keywords')


    class Meta:
        verbose_name = 'Kitab'
        verbose_name_plural = 'Kitablar'

    def __str__(self):
        cat = self.category.title if getattr(self.category, 'title', None) else "—"
        sub = self.sub_category.title if getattr(self.sub_category, 'title', None) else "—"
        status = "✅ Aktiv" if self.is_active else "❌ Passiv"
        price_info = f"{self.price}₼" if self.price else "—"
        if self.old_price:
            price_info += f" (Köhnə: {self.old_price}₼)"
        return f"{self.title or 'Ad yoxdur'} | {cat} > {sub} | {price_info} | {status} | Baxış: {self.views_count}"
# ≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
# Index

class IndexSlider(models.Model):
    title_1 = models.TextField(null=True, blank=True, verbose_name='Başlıq birinci')
    title_2 = models.TextField(null=True, blank=True, verbose_name='Başlıq ikinci')
    description = models.TextField(null=True, blank=True, verbose_name='Məzmun')
    url_title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Url Başlığı')
    url = models.URLField(null=True, blank=True, verbose_name='URL')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    image_2 = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Kiçik şəkil')
    image_2_title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Kiçik şəkil birinci yazısı')
    image_2_title_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Kiçik şəkil ikinci yazısı')
    image_3_title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Kiçik şəkil hərəkətli yazısı')

    class Meta:
        verbose_name='Ana səhifə Slider'
        verbose_name_plural='Ana səhifə Slider'



class IndexBooks(models.Model):
    books = models.ManyToManyField(Book, null=True, blank=True, verbose_name='Kitablar')
    title_1 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq bikinci')
    title_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq ikinci')
    
    def __str__(self):
        return f"{self.title_1 or 'Başlıqsız'}"

    class Meta:
        verbose_name='Ana səhifə Ödənişli Kitablar'
        verbose_name_plural='Ana Səhifə Ödənişli Kitablar'



class IndexPDFBooks(models.Model):
    books = models.ManyToManyField(PDF, null=True, blank=True, verbose_name='Kitablar')
    title_1 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq bikinci')
    title_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq ikinci')
    
    def __str__(self):
        return f"{self.title_1 or 'Başlıqsız'}"

    class Meta:
        verbose_name='Ana səhifə Ödənişsiz Kitablar'
        verbose_name_plural='Ana Səhifə Ödənişsiz Kitablar'






class MetaTags(models.Model):
    PAGE_CHOICES = [
        # --- info app ---
        ('faq', 'FAQ'),
        ('contact', 'Əlaqə'),
        ('about', 'Haqqımızda'),
        ('pdf', 'PDF Səhifəsi'),
        ('search', 'Axtarış Nəticəsi'),

        # --- exam app ---
        ('exam_list', 'İmtahan Siyahısı'),
        ('take_exam', 'İmtahan Hissəsi'),
        ('exam_finish', 'İmtahan Nəticə'),
        ('exam_review', 'İmtahan Rəy Yaz'),
        ('exam_comments', 'İmtahan Rəyləri'),
        ('exam_detail', 'İmtahan Məlumatı'),
        

        # --- main app ---
        ('news', 'Xəbərlər'),
        ('news_details', 'Xəbər Detalı'),
        ('books', 'Kitablar'),
        ('book_details', 'Kitab Detalı'),
        ('index', 'Ana Səhifə'),

        # --- user app ---
        ('cart', 'Səbət'),
        ('login', 'Daxil ol'),
        ('register', 'Qeydiyyatdan keç'),
        ('verify_email', 'Email Təsdiqi'),
        ('account', 'Hesabım'),
        ('password_reset', 'Şifrə Yenilə'),
        ('password_reset_verify', 'OTP Təsdiqi'),
        ('password_reset_confirm', 'Şifrə Yeniləmə'),

        # --- video app ---
        ('video_list', 'Videolar'),
        ('video_info', 'Video Haqqında'),
        ('free_video', 'Pulsuz Videolar'),
        ('video_detail', 'Video Detalı'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, verbose_name='Səhifə')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    keywords = models.TextField(blank=True, null=True, verbose_name='Keywords')

    def __str__(self):
        return self.get_page_display()

    class Meta:
        verbose_name = 'Saytın Meta Başlığı'
        verbose_name_plural = 'Saytın Meta Başlıqları'