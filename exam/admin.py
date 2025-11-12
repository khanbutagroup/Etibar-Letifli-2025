from django.contrib import admin
from exam.models import *
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from django.utils.html import format_html

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
    list_display = ('title', 'is_main', 'sub_sub_sub_category', 'price', 'row_number', 'right_number', 'calculation_types', 'question_honey')
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



# --- 1. Əvvəlcə inline model ---
class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = (
        'question_text',
        'question_points',
        'selected_option',
        'correct_option_display',
        'is_correct',
    )
    can_delete = False

    def question_text(self, obj):
        if not obj.id:
            return None
        return obj.question.title_quest
    question_text.short_description = "Sual mətni"

    def question_points(self, obj):
        if not obj.id:
            return None
        return obj.question.points
    question_points.short_description = "Sualın balı"

    def correct_option_display(self, obj):
        """Düzgün cavabı göstər."""
        if not obj.id:
            return None
        q = obj.question
        for opt in ['A', 'B', 'C', 'D', 'E', 'F']:
            if getattr(q, f'is_correct_{opt.lower()}'):
                return opt
        return None
    correct_option_display.short_description = "Düzgün cavab"

    def is_correct(self, obj):
        """İstifadəçinin cavabı doğrudurmu."""
        if not obj.id:
            return None
        q = obj.question
        selected = obj.selected_option.lower()
        return getattr(q, f'is_correct_{selected}', False)
    is_correct.boolean = True
    is_correct.short_description = "Düzdür?"


# --- 2. Sonra əsas admin ---
@admin.register(UserExamSession)
class UserExamSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'exam_score', 'started_at', 'finished_at')
    readonly_fields = ('user', 'exam', 'exam_details', 'started_at', 'finished_at', 'exam_score')
    inlines = [UserAnswerInline]  # indi tanıyacaq ✅

    def exam_details(self, obj):
        exam = obj.exam
        details = (
            f"İmtahanın adı: {exam.title}\n"
            f"Kateqoriya: {exam.sub_sub_sub_category}\n"
            f"Sual balı: {exam.question_honey}\n"
            f"Qiymət: {exam.price or '—'} AZN\n"
            f"Hesablama tipi: {exam.get_calculation_types_display()}\n"
            f"Müddət: {exam.duration_minutes or '—'} dəqiqə\n"
            f"Başlama tarixi: {exam.start_date or '—'}\n"
            f"Bitmə tarixi: {exam.end_date or '—'}"
        )
        return format_html("<pre style='font-family:monospace; white-space:pre-wrap;'>{}</pre>", details)

    exam_details.short_description = "İmtahan məlumatı"

    def exam_score(self, obj):
        answers = obj.answers.all()
        total_points = sum(a.question.points for a in answers)
        gained_points = sum(a.question.points for a in answers if getattr(a.question, f'is_correct_{a.selected_option.lower()}', False))
        return f"{gained_points} / {total_points} bal"
    exam_score.short_description = "Nəticə"




@admin.register(PurchasedExam)
class PurchasedExamAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'exam_display', 'purchased_at', 'started_at', 'finished_at')
    list_filter = ('purchased_at',)
    search_fields = ('user__username', 'exam__title')
    autocomplete_fields = ('user', 'exam')

    def user_display(self, obj):
        return obj.user.username
    user_display.short_description = "İstifadəçi"

    def exam_display(self, obj):
        return obj.exam.title
    exam_display.short_description = "İmtahan"