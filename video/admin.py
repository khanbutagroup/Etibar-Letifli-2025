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