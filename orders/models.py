from django.db import models
from shop import models as shope_models
from django.contrib.auth import get_user_model
from django.shortcuts import  reverse
User = get_user_model()


class Order(models.Model):
    CHOICE_FIELD = (
        ("none", "none"),
        ("canceled", "canceled"),
        ("paid", "paid"),
        ("done", "done"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=CHOICE_FIELD, default="none")
    pay_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.id} for {self.user.username}"
    @property
    def total_price(self):
        return sum(item.price*item.quantity for item in self.items.all())
    def get_absolute_url(self):
        return reverse('order_list',args=[self.id])

class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    product = models.OneToOneField(shope_models.Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def get_remove_url(self):
        return reverse("remove-orderitem", args=[f"{self.id}"])


class Payment(models.Model):
    CHOICE_FIELD = (
        ("none", "none"),
        ("init", "init"),
        ("processing", "processing"),
        ("rejected", "rejected"),
        ("completed", "completed"),
    )
    ref_id = models.CharField(max_length=1023, default="", null=True)
    trx_id = models.CharField(max_length=1023, default="", null=True)
    order = models.ForeignKey(
        "Order", related_name="payments", on_delete=models.DO_NOTHING
    )
    amount = models.FloatField(default=0, null=True)
    status = models.CharField(default="none", choices=CHOICE_FIELD)
    status_code = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_created=True)
    expires_at = models.DateTimeField(default=None)
    pay_at = models.DateTimeField(auto_now=True)
    gateway = models.CharField(max_length=127)
