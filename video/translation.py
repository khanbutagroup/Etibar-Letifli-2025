from video.models import *
from modeltranslation.translator import TranslationOptions, register

@register(VideoCategory)
class VideoCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(VideoSubCategory)
class VideoSubCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
    
@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title',  'instructions', 'subscription_info', 'active_period', 'instructions_small')

@register(FreeVideo)
class FreeVideoTranslationOptions(TranslationOptions):
    fields = ('title',)