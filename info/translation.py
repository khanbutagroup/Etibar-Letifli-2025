from info.models import *
from modeltranslation.translator import TranslationOptions, register


@register(QuestAnswer)
class QuestAnswerTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Questions)
class QuestionsTranslationOptions(TranslationOptions):
    fields = ('title_image',)

@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('location',)


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'statistic_1_title', 'statistic_1_description', 'statistic_2_title', 'statistic_2_description')


@register(Statistic)
class StatisticTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(AboutTwoStatistic)
class AboutTwoStatisticTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(AboutTwo)
class AboutTwoTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(PDF)
class PdfTranslationOptions(TranslationOptions):
    fields = ('title', 'title_2')

@register(LogoFavicon)
class LogoFaviconTranslationOptions(TranslationOptions):
    fields = ('footer_description',)