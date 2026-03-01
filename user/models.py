import random

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

PURPOSE_CHOICES = (
    ('register', 'Register'),
    ('reset', 'Password Reset'),
)

class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='register')

    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def __str__(self):
        return f"{self.user.email} - {self.purpose} - {self.otp}"


        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Profile"









class PrivacyPolicy(models.Model):
    title = RichTextField(null=True, blank=True, verbose_name='Başlıq')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')

    class Meta:
        verbose_name='Məxfilik Siyasəti'
        verbose_name_plural='Məxfilik Siyasəti'



class SiteInfo(models.Model):
    title = RichTextField(null=True, blank=True, verbose_name='Başlıq')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')

    class Meta:
        verbose_name='İsdifadə Qaydaları'
        verbose_name_plural='İsdifadə Qaydaları'


class ReturnPolicy(models.Model):
    title = RichTextField(null=True, blank=True, verbose_name='Başlıq')
    description = RichTextField(null=True, blank=True, verbose_name='Məzmun')

    class Meta:
        verbose_name='Geri Qaytarma Siyasəti'
        verbose_name_plural='Geri Qaytarma Siyasəti'