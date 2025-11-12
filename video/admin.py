from video.models import *
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationTabularInline



@admin.register(VideoCategory)
class VideoCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'id')
    search_fields = ('title', 'id')

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(VideoSubCategory)
class VideoSubCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'id')
    search_fields = ('title', 'id')

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'sub_category', 'price', 'old_price')
    search_fields = ('title', 'categpry', 'sub_category', 'price', 'old_price')

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(FreeVideo)
class FreeVideoAdmin(TranslationAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'created_at')

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }




@admin.register(PurchasedVideo)
class PurchasedVideoAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'video_display', 'purchased_at', 'expires_at', 'is_active_display')
    list_filter = ('purchased_at',)
    search_fields = ('user__username', 'video__title')
    autocomplete_fields = ('user', 'video')

    def user_display(self, obj):
        return obj.user.username
    user_display.short_description = "İstifadəçi"

    def video_display(self, obj):
        return obj.video.title
    video_display.short_description = "Video"

    def is_active_display(self, obj):
        return obj.video.is_active
    is_active_display.short_description = "Aktivdirmi?"
    is_active_display.boolean = True