from django.db.models import Prefetch
from .models import Category, Product


def root_categories(request):
    return {
        "root_categories": Category.objects.filter(
            root_menu_order__gt=0
        ).order_by('root_menu_order').prefetch_related(
            "subcategories__subcategories__products",
            "subcategories__products",
            "subcategories__subcategories",
            "subcategories",
        )
    }
