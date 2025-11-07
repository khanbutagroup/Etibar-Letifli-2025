from exam.models import *
from modeltranslation.translator import TranslationOptions, register

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(SubSubCategory)
class SubSubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(SubSubSubCategory)
class SubSubSubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Exam)
class ExamTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(QuestionAnswer)
class QuestionAnswerTranslationOptions(TranslationOptions):
    fields = ('title_quest', 'title_a',  'title_b',  'title_c',  'title_d',  'title_e',  'title_f', 'explanation')

