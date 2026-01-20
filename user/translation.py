from modeltranslation.translator import register, TranslationOptions
from .models import PrivacyPolicy, SiteInfo, ReturnPolicy

@register(PrivacyPolicy)
class PrivacyPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # Tərcümə olunacaq sahələr

@register(SiteInfo)
class SiteInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(ReturnPolicy)
class ReturnPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
