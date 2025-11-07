from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Mövcud UserAdmin-a profile əlavə et
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Django default User admin-u unregister et və yenidən register et
admin.site.unregister(User)
admin.site.register(User, UserAdmin)