from django.db.models import Prefetch
from . import models


def orders_active(request):

    {
        "orders_active": models.Order.objects.filter(status="none")
        .select_related("user")
        .prefetch_related("items", "payments")
    }
