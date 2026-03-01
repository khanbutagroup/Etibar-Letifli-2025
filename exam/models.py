from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=128, null=True, verbose_name='Başlıq')

    def __str__(self):
        return self.title or "Kateqoriya"

    class Meta:
        verbose_name='Kateqoriya'
        verbose_name_plural='Kateqoriyalar'


class SubCategory(models.Model):
    title = models.CharField(max_length=128, null=True, verbose_name='Başlıq')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='Kateqoriya')


    def __str__(self):
        # Məsələn: "Azərbaycan bölməsi → İbtidai sinif"
        return f"{self.category.title if self.category else '—'} → {self.title or ''}"


    class Meta:
        verbose_name='Alt Kateqoriya'
        verbose_name_plural='Alt Kateqoriyalar'

class SubSubCategory(models.Model):
    title = models.CharField(max_length=128, null=True, verbose_name='Başlıq')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name='Alt Kateqoriya')
    
    def __str__(self):
        # Məsələn: "Azərbaycan bölməsi → İbtidai sinif → Riyaziyyat"
        if self.sub_category and self.sub_category.category:
            return f"{self.sub_category.category.title} → {self.sub_category.title} → {self.title}"
        return self.title or "Alt Alt Kateqoriya"

    class Meta:
        verbose_name='Alt Alt Kateqoriya'
        verbose_name_plural='Alt Alt Kateqoriyalar'

class SubSubSubCategory(models.Model):
    title = models.CharField(max_length=128, null=True, verbose_name='Başlıq')
    sub_sub_category = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, null=True, verbose_name='Alt Alt Kateqoriya')

    def __str__(self):
        # Məsələn: "Azərbaycan bölməsi → İbtidai sinif → Riyaziyyat → Məntiq"
        try:
            cat = self.sub_sub_category.sub_category.category.title
            subcat = self.sub_sub_category.sub_category.title
            subsub = self.sub_sub_category.title
            return f"{cat} → {subcat} → {subsub} → {self.title}"
        except AttributeError:
            return self.title or "Alt Alt Alt Kateqoriya"

    class Meta:
        verbose_name='Alt Alt Alt Kateqoriya'
        verbose_name_plural='Alt Alt Alt Kateqoriyalar'



class Exam(models.Model):
    CALCULATION_TYPES = [
        (1, "Səhvlər düzgünlərə təsir etmir"),
        (2, "Hər səhv öz balının ¼-ni aparır"),
        (3, "Hər 4 səhv 1 düzü aparır"),
    ]

    sub_sub_sub_category = models.ForeignKey(SubSubSubCategory, related_name="exams", on_delete=models.CASCADE, null=True, verbose_name='Alt Alt Alt Kateqoriya')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    title = models.CharField(max_length=256, verbose_name='İmtahanın adı')
    description = models.TextField(null=True, verbose_name='Məzmun')

    # comment = pass
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True, verbose_name='Qiymət')
    # question_count = pass
    row_number = models.PositiveIntegerField(default=0, null=True, verbose_name='Səf sayısı')
    right_number = models.PositiveIntegerField(default=0, null=True, verbose_name='Düz sayısı')
    leads_straight = models.DecimalField(max_digits=5, decimal_places=2, default=0.25, verbose_name='Düz aparır')
    calculation_types = models.PositiveSmallIntegerField(choices=CALCULATION_TYPES, default=1, verbose_name='Hesablama tipləri')
    question_honey = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='Sual Balı')
    video = models.FileField(upload_to='video/', null=True, blank=True, verbose_name='Hədiyə Video')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yaradılma tarixi')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Başlama tarixi')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Bitmə tarixi')
    purchased_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Alındığı tarix')
    started_at = models.DateTimeField(null=True, blank=True)  # istifadəçi imtahana başlayanda qeyd olunur
    finished_at = models.DateTimeField(null=True, blank=True) 


    is_main = models.BooleanField(default=False, null=True, blank=True, verbose_name='Əsas imtahandır? Ana səhifədə')

    # Ödənişdən qabaq məlumatlandırıcı hissə
    # 📆 Aktivlik və müddət
    active_period_days = models.PositiveIntegerField(default=30, verbose_name='Aktiv olma müddəti (günlərlə)')
    active_period = RichTextField(null=True, blank=True, verbose_name='Aktiv olma müddəti yazısı')
    duration_hours = models.PositiveIntegerField(default=0, verbose_name='Davam etmə vaxtı (saat)')
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name='Davam etmə vaxtı (dəqiqə)')

    # 🧾 Təlimat və əlavə məlumat
    instructions = models.TextField(null=True, blank=True, verbose_name='Təlimatlar')
    subscription_info = models.TextField(null=True, blank=True, verbose_name='Yazılış haqqında məlumat')
    instructions_small = models.TextField(null=True, blank=True, verbose_name='Qısa Təlimat yazısı')

    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, null=True, verbose_name='Meta Description')
    meta_keywords = models.TextField(blank=True, null=True, verbose_name='Meta Keywords')

    def has_started(self):
        return self.started_at is not None

    def has_finished(self):
        return self.finished_at is not None


    def is_available(self):
        """Yoxlayır ki, imtahan hazırda aktivdirmi."""
        now = timezone.now()
        # Əgər tarixlər təyin edilməyibsə → imtahan həmişə açıq olsun
        if not self.start_date and not self.end_date:
            return True

        # Əgər yalnız start_date var → start tarixindən sonra həmişə açıq olsun
        if self.start_date and not self.end_date:
            return self.start_date <= now

        # Əgər yalnız end_date var → end_date-dən əvvəl açıq olsun
        if not self.start_date and self.end_date:
            return now <= self.end_date

        # Əgər hər ikisi təyin edilib → normal aralıq yoxlaması
        return self.start_date <= now <= self.end_date


    def __str__(self):
        return self.title or ""

    def logical_calculation(self):
        right = self.right_number
        row = self.row_number
        honey = float(self.question_honey)

        if self.calculation_types == 1:
            final = right * honey
        elif self.calculation_types ==2:
            final = right * honey - row * (honey / 4)
        elif self.calculation_types == 3:
            final = (right - row / 4) * honey
        else:
            final = right * honey

        return round(max(final, 0), 2)

    def get_status_text(self):
        now = timezone.now()

        # Heç bir tarix qoyulmayıbsa — imtahan açıqdır
        if not self.start_date and not self.end_date:
            return "İmtahan aktivdir"

        # Hələ başlamayıbsa
        if self.start_date and now < self.start_date:
            return f"İmtahan {self.start_date.strftime('%d.%m.%Y %H:%M')} tarixində açılacaq"

        # Bitmə tarixi keçibsə
        if self.end_date and now > self.end_date:
            return "İmtahanın aktiv olma vaxtı bitib."

        # Aralıqdadırsa
        return "İmtahana başla"
        
    class Meta:
        verbose_name='İmtahan'
        verbose_name_plural='İmtahanlar'




class QuestionAnswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, related_name="questions_answers", verbose_name='İmtahan')
    image_quest = models.ImageField(upload_to='quest/', null=True, blank=True, verbose_name='Sual şəkli')
    title_quest = models.CharField(max_length=500, null=True, verbose_name='Sual Başlıq')
    points = models.PositiveIntegerField(default=1, verbose_name='Sualın Balı')  # Sualın balı

    # Cavab A
    image_a = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab A Şəkil')
    title_a = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab A Başlıq')
    is_correct_a = models.BooleanField(default=False, verbose_name='Cavab A Düzdür?')

    
    # Cavab B
    image_b = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab B Şəkil')
    title_b = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab B Başlıq')
    is_correct_b = models.BooleanField(default=False, verbose_name='Cavab B Düzdür?')

    
    # Cavab C
    image_c = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab C Şəkil')
    title_c = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab C Başlıq')
    is_correct_c = models.BooleanField(default=False, verbose_name='Cavab C Düzdür?')

    
    # Cavab D
    image_d = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab D Şəkil')
    title_d = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab D Başlıq')
    is_correct_d = models.BooleanField(default=False, verbose_name='Cavab D Düzdür?')

    
    # Cavab E
    image_e = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab E Şəkil')
    title_e = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab E Başlıq')
    is_correct_e = models.BooleanField(default=False, verbose_name='Cavab E Düzdür?')

    
    # Cavab F
    image_f = models.ImageField(upload_to='answer/', null=True, blank=True, verbose_name='Cavab F Şəkil')
    title_f = models.CharField(max_length=500, null=True, blank=True, verbose_name='Cavab F Başlıq')
    is_correct_f = models.BooleanField(default=False, verbose_name='Cavab F Düzdür?')


    explanation = models.TextField(null=True, blank=True, verbose_name='Düz Cavab İzahı')
    def __str__(self):
        return f"{self.title_quest} ({self.exam})"

    class Meta:
        verbose_name='Sual və Cavablar'
        verbose_name_plural='Sual və Cavablar'








class UserExamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    final_points = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def is_finished(self):
        return self.finished_at is not None or self.started_at is not None

    class Meta:
        verbose_name = "İstifadəçi imtahan sessiyası"
        verbose_name_plural = "İstifadəçi imtahan sessiyaları"

class UserAnswer(models.Model):
    session = models.ForeignKey(UserExamSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[
        ('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F')
    ])



class PurchasedExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"




    class Meta:
        unique_together = ('user', 'exam')
        verbose_name = "Alınmış imtahan"
        verbose_name_plural = "Alınmış imtahanlar"

class ExamReview(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='reviews', verbose_name="İmtahan")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="İstifadəçi")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Ulduz sayı (1-5)")
    comment = models.TextField(verbose_name="Rəy mətni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yazılma tarixi")

    def __str__(self):
        return f"{self.user.username} — {self.exam.title} ({self.rating}★)"
    
    class Meta:
        verbose_name = "İmtahan rəyi"
        verbose_name_plural = "İmtahan rəyləri"
        ordering = ['-created_at']




class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)
    
    kb_order_id = models.CharField(max_length=50, null=True, blank=True)
    kb_password = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"{self.user} - {self.exam} - {self.status}"
