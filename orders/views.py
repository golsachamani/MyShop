from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from shop import models as shope_models


class OrderList(LoginRequiredMixin, generic.ListView):
    model = models.Order
    template_name = "order_list.html"
    context_object_name = "orders"

    def get_queryset(self, **kwargs):
        return models.Order.objects.filter(user=self.request.user)


class AddToCart(generic.View):
    model = models.OrderItem

    def post(self, *args, **kwargs):

        product_id = self.kwargs.get("pk")
        product = shope_models.Product.objects.get(pk=product_id)
        form = forms.AddToCartProduct(self.request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            cart = models.Order.objects.filter(
                status="none", user=self.request.user
            ).last()
            if not cart:
                cart = models.Order.objects.create(user=self.request.user)
            orderitem = None
            for item in cart.items.all():
                if item.product.id == product.id:
                    orderitem = item
                    break
            if orderitem:
                orderitem.quantity += quantity
            else:
                orderitem = models.OrderItem.objects.create(
                    product=product, price=product.price, quantity=quantity, order=cart
                )
            orderitem.save()
            cart.save()
        return redirect(product.get_absolute_url())


class RemoveCart(LoginRequiredMixin, generic.DeleteView):
    model = models.OrderItem
    template_name = "delete_item.html"
    context_object_name = "item"
    success_url = reverse_lazy("order_list")

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        item = get_object_or_404(models.OrderItem, pk=pk)
        if item.order.user == self.request.user:
            item.delete()
        return redirect("order_list")
