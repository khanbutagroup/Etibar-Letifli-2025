from django.db import models
from ckeditor.fields import RichTextField

class QuestAnswer(models.Model):
    title = models.TextField(null=True, blank=True, verbose_name='Sual')
    description = models.TextField(null=True, blank=True, verbose_name='Cavab')
    questions = models.ForeignKey('Questions', on_delete=models.CASCADE, null=True, blank=True, related_name='answers', verbose_name='Sual - Cavab')
    class Meta:
        verbose_name='Sual - Cavab'
        verbose_name_plural='Sual - Cavablar'

class Questions(models.Model):
    NUMBER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    number = models.CharField(max_length=1, choices=NUMBER_CHOICES, verbose_name='Sıra')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    title_image = models.CharField(max_length=256, null=True, blank=True, verbose_name='Şəkil başlığı')

    class Meta:
        verbose_name='Sual - Cavab'
        verbose_name_plural='Sual - Cavablar'
    
# Faq
# ≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
# Contact

class Contact(models.Model):
    location = models.TextField(null=True, blank=True, verbose_name='Ünvan')
    location_url = models.TextField(null=True, blank=True, verbose_name='Ünvan Url Map')

    phone_1 = models.CharField(max_length=18, null=True, blank=True, verbose_name='Telefon nömrəsi birinci')
    phone_2 = models.CharField(max_length=18, null=True, blank=True, verbose_name='Telefon nömrəsi ikinci')

    email_1 = models.EmailField(null=True, blank=True, verbose_name='Email birinci')
    email_2 = models.EmailField(null=True, blank=True, verbose_name='Email ikinci')

    class Meta:
        verbose_name='Əlaqə Səhifəsi'
        verbose_name_plural='Əlaqə səhifəsi'


class ContactUser(models.Model):
    first_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Ad')
    last_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Soyad')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    phone = models.CharField(max_length=18, null=True, blank=True, verbose_name='Telefon')
    messages = models.TextField(null=True, blank=True, verbose_name='Mesaj')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaranma tarixi')

    class Meta:
        verbose_name='Əlqə Qurmaq Tələbi'
        verbose_name_plural='Əlaqə Qurmaq Tələbəri'


class SosialAccount(models.Model):
    facebook = models.URLField(null=True, blank=True, verbose_name='Facebook')
    instagram = models.URLField(null=True, blank=True, verbose_name='İnstagram')
    linkedin = models.URLField(null=True, blank=True, verbose_name='Linkedin')
    whatsapp = models.CharField(max_length=128, null=True, blank=True, verbose_name='Whatsapp')
    tiktok = models.URLField(null=True, blank=True, verbose_name='Tiktok')
    telegram = models.URLField(null=True, blank=True, verbose_name='Telegram')
    youtube = models.URLField(null=True, blank=True, verbose_name='Youtube')

    class Meta:
        verbose_name='Sosial Akkount'
        verbose_name_plural='Sosial Akkountlar'

# ≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
# About

class About(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Başlıq')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Əsas şəkil')
    image_2 = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Əsas hərəkətli icon')
    image_2_title_1 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Əsas hərəkətli icon yazısı birinci')
    image_2_title_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Əsas hərəkətli icon yazısı ikinci')

    image_3 = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Əsas icon 2')
    image_4 = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Əsas icon 3')

    statistic_1_title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Birinci statistika başlıq')
    statistic_1_description = models.CharField(max_length=128, null=True, blank=True, verbose_name='Birinci statistika məzmun')
    statistic_1_icon = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Birinci statistika Şəkli')

    statistic_2_title = models.CharField(max_length=128, null=True, blank=True, verbose_name='İkinci statistika başlıq')
    statistic_2_description = models.CharField(max_length=128, null=True, blank=True, verbose_name='İkinci statistika məzmun')
    statistic_2_icon = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='İkinci statistika Şəkli')

    class Meta:
        verbose_name='Haqqımızda birinci hissə'
        verbose_name_plural='Haqqımızda birinci hissə'





class Statistic(models.Model):
    digit = models.CharField(max_length=256, null=True, blank=True, verbose_name='Rəqəm')
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')

    class Meta:
        verbose_name='Statistika'
        verbose_name_plural='Statistikalar'


class AboutTwoStatistic(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Başlıq')
    description = models.TextField(null=True, blank=True, verbose_name='Məzmun')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='İcon')
    about_two = models.ForeignKey('AboutTwo', on_delete=models.CASCADE, null=True, blank=True, related_name='about', verbose_name='Haqqımızda')
    class Meta:
        verbose_name='Haqqımızda ikinci hissə statistika'
        verbose_name_plural='Haqqımızda ikinci hissə statistikalar'


class AboutTwo(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')

    class Meta:
        verbose_name='Haqqımızda ikinci hissə'
        verbose_name_plural='Haqqımızda ikinci hissə'


# ≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
# Pdf


class PDF(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Başlıq')
    title_2 = models.CharField(max_length=256, null=True, blank=True, verbose_name='Başlıq 2')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    pdf = models.FileField(upload_to='pdf/', null=True, blank=True, verbose_name='PDF')
    is_active = models.BooleanField(default=True, verbose_name='Aktivdirmi?')

    class Meta:
        verbose_name='PDF'
        verbose_name_plural='PDF-lər'
    def __str__(self):
        # status (aktiv / passiv)
        status = "🟢 Aktiv" if self.is_active else "🔴 Passiv"

        # şəkil və pdf məlumatı
        image_info = f"📷 var" if self.image else "📷 yoxdur"
        pdf_info = f"📄 {self.pdf.name.split('/')[-1]}" if self.pdf else "📄 yoxdur"

        # əsas başlıqlar
        main_title = self.title or "Başlıq yoxdur"
        second_title = f" | {self.title_2}" if self.title_2 else ""

        return f"{main_title}{second_title} | {pdf_info} | {image_info} | {status}"


class LogoFavicon(models.Model):
    header_logo = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Header Logo')
    footer_logo = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Footer Logo')
    footer_description = models.TextField(null=True, blank=True, verbose_name='Footer loqo altı Məzmun')
    favicon = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Favicon')

    class Meta:
        verbose_name='Loqo və Favicon'
        verbose_name_plural='Loqo və Favicon'

    
class Subscribe(models.Model):
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Abonə olma tarixi')

    def __str__(self):
        return self.email or " "

    class Meta:
        verbose_name='Abonə Olanlar'
        verbose_name_plural='Abonə Olanlar'




class BookFreeCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')

    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='Sual Kitabçaları Kateqoriyası'
        verbose_name_plural='Sual Kitabçaları Kateqoriyaları'


class BookFree(models.Model):
    category = models.ForeignKey(BookFreeCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')
    title = models.TextField(null=True, blank=True, verbose_name='Başlıq')
    image = models.ImageField(upload_to='bookfree/', null=True, blank=True, verbose_name='Şəkil')
    pdf = models.FileField(upload_to='prf/', null=True, blank=True, verbose_name='PDF')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaranma tarixi')
 
    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='Sual Kitabçaları'
        verbose_name_plural='Sual Kitabçaları'




class TestCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')

    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='Test Kateqoriyası'
        verbose_name_plural='Test Kateqoriyaları'






class Test(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')
    title = models.TextField(null=True, blank=True, verbose_name='Başlıq')
    image = models.ImageField(upload_to='bookfree/', null=True, blank=True, verbose_name='Şəkil')
    pdf = models.FileField(upload_to='prf/', null=True, blank=True, verbose_name='PDF')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaranma tarixi')

    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='Test'
        verbose_name_plural='Testlər'


class ExpanationCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')

    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='İzah Kateqoriyası'
        verbose_name_plural='İzah Kateqoriyaları'

class Expanation(models.Model):
    category = models.ForeignKey(ExpanationCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')
    title = models.TextField(null=True, blank=True, verbose_name='Başlıq')
    image = models.ImageField(upload_to='bookfree/', null=True, blank=True, verbose_name='Şəkil')
    pdf = models.FileField(upload_to='prf/', null=True, blank=True, verbose_name='PDF')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaranma tarixi')

    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='İzah'
        verbose_name_plural='İzahlar'


class FeatureItem(models.Model):
    title_1 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq bikinci')
    title_2 = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq ikinci')
    books = models.ManyToManyField('BookFree', blank=True, verbose_name='Sual Kitabçaları')
    tests = models.ManyToManyField('Test', blank=True, verbose_name='Testlər')
    explanations = models.ManyToManyField('Expanation', blank=True, verbose_name='İzahlar')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ana Səhifə Pulsuz resurslar'
        verbose_name_plural = 'Ana Səhifə Pulsuz resurslar'


# Constant seçimlər
CONTENT_TYPE_CHOICES = [
    ('video', 'Video Dərslər'),
    ('exam', 'Online İmtahanlar'),
]

class Course(models.Model):
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='video', verbose_name="Məzmun Növü")
    description = RichTextField(blank=True, verbose_name="Təsvir")

    class Meta:
        verbose_name='İsdifadəçiyə məlumat mesajı'
        verbose_name_plural='İsdifadəçiyə məlumat mesajı'
