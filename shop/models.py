from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models.functions import Coalesce
from django.db.models import Value as V

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=127)
    slug = models.SlugField(unique=True, max_length=127)
    parent = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="subcategories",
        blank=True,
        null=True,
    )
    img = models.ImageField(upload_to="category/", blank=True, null=True)
    root_menu_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def path(self):
        parts = [self.slug]
        parent = self.parent
        while parent:
            parts.insert(0, parent.slug)
            parent = parent.parent
        return "/".join(parts)

    def get_absolute_url(self):
        return reverse("category_detail", args=[self.path])

    def get_descendants(self):
        descendants = []

        for child in self.subcategories.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())

        return descendants


class Brand(models.Model):
    name = models.CharField(max_length=127, unique=True)
    desc = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="brands/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    price = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    desc = models.TextField(null=True, blank=True)
    variant_of = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="variants",
        null=True,
        blank=True,
    )
    stock = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_special_offer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={
                "category_path": self.category.path,
                "product_slug": self.slug,
            },
        )

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg("rating"))["rating__avg"]
        return 0

    @staticmethod
    def filter_and_sort(qs, filters=None, order_by_attr=None, order="asc"):
        if filters:
            for attr_name, values in filters.items():
                qs = qs.filter(
                    attributes__attribute__name=attr_name,
                    attributes__value__in=values,
                )
        if order_by_attr:

            qs = qs.filter(attributes__attribute__name=order_by_attr)
            is_numeric = order_by_attr.lower() in ["ram", "storage", "weight", "price"]
            if is_numeric:
                qs = qs.annotate(
                    sort_value=Cast(F("attributes__value"), IntegerField())
                )
            else:
                qs = qs.annotate(sort_value=Coalesce(F("attributes__value"), V("")))

            if order == "asc":
                qs = qs.order_by("sort_value")
            else:
                qs = qs.order_by("-sort_value")

        return qs

    @staticmethod
    def get_attributes_options(products_qs):
        options = {}
        for product in products_qs:
            for attr in product.attributes.all():
                name = attr.attribute.name
                if name not in options:
                    options[name] = set()
                options[name].add(attr.value)
        sorted_options = {}
        for key, value_set in options.items():
            sorted_options[key] = sorted(list(value_set))

        return sorted_options
    @property
    def stock_status(self):
        if self.stock > 5:
            return "in_stock"
        elif self.stock > 0:
            return "low_stock"
        return "out_of_stock"


class ProductImage(models.Model):
    img = models.ImageField(upload_to="products/", blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    is_main = models.BooleanField(default=False)


class Attribute(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="attributes"
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"


class Banner(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, null=True, blank=True
    )

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_target_url(self):
        if self.product:
            return self.product.get_absolute_url()
        if self.category:
            return self.category.get_absolute_url()
        return self.link

    def __str__(self):
        return self.title
