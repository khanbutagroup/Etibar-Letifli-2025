from django.db import models
from django.contrib.auth.models import User
import random

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