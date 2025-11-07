from info.models import *
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationTabularInline


class QuestAnswerInline(TranslationTabularInline):
    model = QuestAnswer
    extra = 1

@admin.register(Questions)
class QuestionsAdmin(TranslationAdmin):
    inlines = [QuestAnswerInline]
    list_display = ('number', 'title_image')
    search_fields = ('number', 'title_image')

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


@admin.register(Contact)
class ContactAdmin(TranslationAdmin):
    list_display = ('location', 'phone_1', 'phone_2', 'email_1', 'email_2')
    search_fields = ('location', 'phone_1', 'phone_2', 'email_1', 'email_2')

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

@admin.register(ContactUser)
class ContactUserAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'last_name', 'email', 'phone', 'messages')
    search_fields = ('created_at', 'first_name', 'last_name', 'email', 'phone', 'messages')


@admin.register(SosialAccount)
class SosialAccountAdmin(admin.ModelAdmin):
    list_display = ('facebook', 'instagram', 'linkedin', 'whatsapp', 'tiktok', 'telegram', 'youtube')
    search_fields = ('facebook', 'instagram', 'linkedin', 'whatsapp', 'tiktok', 'telegram', 'youtube')



@admin.register(About)
class AboutAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'statistic_1_title', 'statistic_2_title')
    search_fields = ('title', 'description', 'statistic_1_title', 'statistic_2_title')

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

@admin.register(Statistic)
class StatisticAdmin(TranslationAdmin):
    list_display = ('digit', 'title')
    search_fields = ('digit', 'title')

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


class AboutTwoStatisticInline(TranslationTabularInline):
    model = AboutTwoStatistic
    extra = 1

@admin.register(AboutTwo)
class AboutTwoAdmin(TranslationAdmin):
    inlines = [AboutTwoStatisticInline]
    list_display = ('title',)
    search_fields = ('title',)

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

@admin.register(PDF)
class PDFAdmin(TranslationAdmin):
    list_display = ('title', 'title_2', 'pdf', 'is_active')
    search_fields = ('title', 'title_2', 'pdf', 'is_active')

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


@admin.register(LogoFavicon)
class LogoFaviconAdmin(TranslationAdmin):
    list_display = ('id', 'footer_description')
    search_fields = ('id', 'footer_description')

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


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email', 'created_at')

    