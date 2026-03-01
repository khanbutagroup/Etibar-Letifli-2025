from main.models import *
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationTabularInline


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'created_at', 'is_active')
    search_fields = ('title', 'created_at', 'is_active')

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


@admin.register(BookCategory)
class BookCategoryAdmin(TranslationAdmin):
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

@admin.register(BookSubCategory)
class BookSubCategoryAdmin(TranslationAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category')

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


@admin.register(Book)
class BookAdmin(TranslationAdmin):
    list_display = (
        'title', 
        'category', 
        'sub_category',
        'price', 
        'old_price', 
        'views_count', 
        'is_active', 
        'created_at'
    )
    list_filter = ('category', 'sub_category', 'is_active')
    search_fields = ('title', 'ticket')
    readonly_fields = ('views_count', 'created_at')
    list_editable = ('price', 'old_price', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'category', 
                'sub_category', 
                'description', 
                'ticket', 
                'image', 
                'price', 
                'old_price', 
                'sample_pages', 
                'answers', 
                'is_active'
            )
        }),
        ('Advanced info', {
            'classes': ('collapse',),
            'fields': ('views_count', 'created_at'),
        }),
    )

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



@admin.register(IndexSlider)
class IndexSliderAdmin(TranslationAdmin):
    list_display = ('title_1', 'title_2', 'url_title', 'image_2_title', 'image_2_title_2')
    search_fields = ('title_1', 'title_2', 'url_title', 'image_2_title', 'image_2_title_2')

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


@admin.register(IndexBooks)
class IndexBooksAdmin(TranslationAdmin):
    list_display = ('get_books', 'title_1', 'title_2')
    search_fields = ('title_1', 'title_2', 'books__title')

    filter_horizontal = ('books',)  # çoxlu seçim üçün rahat interfeys

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    get_books.short_description = 'Kitablar'

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




# @admin.register(IndexPDFBooks)
# class IndexPDFBooksAdmin(TranslationAdmin):
#     list_display = ('get_books', 'title_1', 'title_2')
#     search_fields = ('title_1', 'title_2', 'books__title')

#     filter_horizontal = ('books',)  # çoxlu seçim üçün rahat interfeys

#     def get_books(self, obj):
#         return ", ".join([book.title for book in obj.books.all()])
#     get_books.short_description = 'Kitablar'

#     group_fieldsets = True
#     class Media:
#         js = (
#             'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
#             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
#             'modeltranslation/js/tabbed_translation_fields.js',
#         )
#         css = {
#             'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
#         }


@admin.register(CartQuantityDiscount)
class CartQuantityDiscountAdmin(admin.ModelAdmin):
    list_display = (
        'min_quantity',
        'max_quantity',
        'discount_percent',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    list_editable = (
        'discount_percent',
        'is_active',
    )

    ordering = (
        'min_quantity',
    )

    fieldsets = (
        ('Miqdar aralığı', {
            'fields': (
                'min_quantity',
                'max_quantity',
            )
        }),
        ('Endirim məlumatı', {
            'fields': (
                'discount_percent',
                'is_active',
            )
        }),
    )



@admin.register(DeliveryPrice)
class DeliveryPriceAdmin(admin.ModelAdmin):
    list_display = (
        "min_quantity",
        "max_quantity",
        "price",
        "is_active",
    )

    list_filter = ("is_active",)
    search_fields = ("min_quantity", "max_quantity")
    ordering = ("min_quantity",)

    list_editable = ("price", "is_active")

    fieldsets = (
        (None, {
            "fields": ("min_quantity", "max_quantity", "price")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.min_quantity > obj.max_quantity:
            from django.core.exceptions import ValidationError
            raise ValidationError("Minimum say maksimum saydan böyük ola bilməz.")
        super().save_model(request, obj, form, change)