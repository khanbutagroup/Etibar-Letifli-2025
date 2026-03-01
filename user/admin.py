from django.contrib import admin
from user.models import *
# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile
from modeltranslation.admin import TranslationAdmin
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



@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(TranslationAdmin):
    group_fieldsets = True
    list_display = ('title', 'description')  # title və description sütunları admin siyahısında
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(SiteInfo)
class SiteInfoAdmin(TranslationAdmin):
    group_fieldsets = True
    list_display = ('title', 'description')
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(TranslationAdmin):
    group_fieldsets = True
    list_display = ('title', 'description')
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }