from main.models import *
from modeltranslation.translator import TranslationOptions, register

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'meta_title', 'meta_description', 'meta_keywords')

@register(BookCategory)
class BookCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(BookSubCategory)
class BookSubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'ticket', 'meta_title', 'meta_description', 'meta_keywords')

@register(IndexSlider)
class IndexSliderTranslationOptions(TranslationOptions):
    fields = ('title_1', 'title_2', 'description', 'url_title', 'image_2_title', 'image_2_title_2', 'image_3_title')

@register(IndexBooks)
class IndexBooksTranslationOptions(TranslationOptions):
    fields = ('title_1', 'title_2')

@register(IndexPDFBooks)
class IndexPDFBooksTranslationOptions(TranslationOptions):
    fields = ('title_1', 'title_2')