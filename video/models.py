from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone



class VideoCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Video Kateqoriyası'
        verbose_name_plural='Video Kateqoriyaları'



class VideoSubCategory(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Video Sub Kateqoriyası'
        verbose_name_plural='Video Sub Kateqoriyaları'



class Video(models.Model):
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kateqoriya')
    sub_category = models.ForeignKey(VideoSubCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Sub kateqoriya')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Video Şəkli')
    video = models.FileField(upload_to='video/', null=True, blank=True, verbose_name='Video')
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Başlıq')
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True, verbose_name='Qiymət')
    old_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True, verbose_name='Köhnə qiymət')

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
    # ⚙️ Digər məlumatlar
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yaradılma tarixi')
    is_active = models.BooleanField(default=True, verbose_name='Aktivdirmi?')


    def __str__(self):
        return self.title or " "

    class Meta:
        verbose_name='Video'
        verbose_name_plural='Videolar'



class FreeVideo(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name='Başlıq')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Şəkil')
    video = models.URLField(null=True, blank=True, verbose_name='Video')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir?')
    class Meta:
        verbose_name='Ödənişsiz videolar'
        verbose_name_plural='Ödənişsiz videolar'







class PurchasedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_videos')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        """İstifadəçinin videoya baxış icazəsi aktivdirmi."""
        if not self.expires_at:
            return True
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"

    class Meta:
        verbose_name = "Alınmış video"
        verbose_name_plural = "Alınmış videolar"