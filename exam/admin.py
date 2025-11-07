from django.contrib import admin
from exam.models import *
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline


# Category admin
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
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

@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'category',)
    list_filter = ('category',)
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

@admin.register(SubSubCategory)
class SubSubCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'sub_category',)
    list_filter = ('sub_category',)
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

@admin.register(SubSubSubCategory)
class SubSubSubCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'sub_sub_category',)
    list_filter = ('sub_sub_category',)
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



class QuestionAnswerInline(TranslationStackedInline):
    model = QuestionAnswer
    extra = 1
    fieldsets = (
        ('Sual', {
            'fields': ('title_quest', 'image_quest', 'points', 'explanation'),
        }),
        ('Cavab A', {'fields': ('title_a', 'is_correct_a')}),
        ('Cavab B', {'fields': ('title_b', 'is_correct_b')}),
        ('Cavab C', {'fields': ('title_c', 'is_correct_c')}),
        ('Cavab D', {'fields': ('title_d', 'is_correct_d')}),
        ('Cavab E', {'fields': ('title_e', 'is_correct_e')}),
        ('Cavab F', {'fields': ('title_f', 'is_correct_f')}),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

# Exam admin
@admin.register(Exam)
class ExamAdmin(TranslationAdmin):
    list_display = ('title', 'sub_sub_sub_category', 'price', 'row_number', 'right_number', 'calculation_types', 'question_honey')
    list_filter = ('sub_sub_sub_category', 'calculation_types',)
    search_fields = ('title',)
    inlines = [QuestionAnswerInline]
    exclude = ('started_at', 'finished_at')
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