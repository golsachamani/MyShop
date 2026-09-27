from django.contrib import admin
from django.utils.html import format_html
from . import models


# ================= SubCategory Inline =================
class SubCategoryInline(admin.TabularInline):
    model = models.Category
    fk_name = "parent"
    extra = 1


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    list_display = ("name", "parent")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]


# ================= Product Image Inline =================
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ("preview",)
    extra = 1

    def preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="80" />', obj.img.url)
        return "-"


# ================= Product Attribute Inline =================
class ProductAttributeInline(admin.TabularInline):
    model = models.ProductAttribute
    extra = 1


# ================= Product Review Inline =================
class ProductReviewInline(admin.TabularInline):
    model = models.ProductReview
    readonly_fields = ("user", "created_at")
    extra = 0
    max_num = 0


# ================= Product Admin =================
@admin.register(models.Product)
class Product(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "category", "brand"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProductImageInline,
        ProductReviewInline,
        ProductAttributeInline,
    ]


# ================= Brand Admin =================
@admin.register(models.Brand)
class Brand(admin.ModelAdmin):
    list_display = ["id", "name"]


# ================= Attribute Admin =================
@admin.register(models.Attribute)
class Attribute(admin.ModelAdmin):
    list_display = ("name", "category")


@admin.register(models.ProductReview)
class ProductReview(admin.ModelAdmin):
    list_display = ["id", "user", "product"]


# ================= Banner Admin =================
@admin.register(models.Banner)
class Banner(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")
