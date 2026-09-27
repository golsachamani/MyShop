from rest_framework import generics
from . import models
from . import serializers
from django.shortcuts import get_object_or_404, redirect



class FeaturedProductList(generics.ListAPIView):
    model = models.Product
    serializer_class = serializers.Product

    def get_queryset(self):
        return models.Product.objects.filter(is_featured=True, variant_of__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Featured Products"
        return context


class NewProductList(generics.ListAPIView):
    model = models.Product
    serializer_class = serializers.Product

    def get_queryset(self):
        return models.Product.objects.filter(is_new=True, variant_of__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "New Products"


class SpecialOfferList(generics.ListAPIView):
    model = models.Product
    serializer_class = serializers.Product

    def get_queryset(self):
        return models.Product.objects.filter(
            is_special_offer=True, variant_of__isnull=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Special Offers"
        return context


class ProductDetail(generics.RetrieveAPIView):
    model = models.Product
    serializer_class = serializers.Product

    def get_object(self):
        category_path = self.kwargs.get("category_path")
        product_slug = self.kwargs.get("product_slug")
        slugs = category_path.split("/")
        parent = None
        category = None
        for slug in slugs:
            category = get_object_or_404(models.Category, parent=parent, slug=slug)
            parent = category

        product = get_object_or_404(
            models.Product, slug=product_slug, category=category
        )
        return product

class CategoryDetail(generics.RetrieveAPIView):
    model = models.Category
    serializer_class = serializers.Category
    

    def get_object(self):
        category_path = self.kwargs.get("category_path", "").rstrip("/")
        parent = None
        cat = None

        for slug in category_path.split("/"):
            cat = get_object_or_404(models.Category, slug=slug, parent=parent)
            parent = cat

        return cat