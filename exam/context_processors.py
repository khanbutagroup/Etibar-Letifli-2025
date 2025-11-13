# exam/context_processors.py
from exam.models import Category

def exam_categories(request):
    """
    Bütün kateqoriyaları və onların alt səviyyələrini (SubCategory, SubSubCategory, SubSubSubCategory)
    qlobal şəkildə bütün templatelərə ötürür.
    """
    categories = (
        Category.objects.prefetch_related(
            'subcategory_set__subsubcategory_set__subsubsubcategory_set'
        )
        .all()
        .order_by('title')
    )

    return {
        'all_categories': categories
    }

