from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from orders import forms as orders_form
from . import models, forms


class Home(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_products = models.Product.objects.filter(
            variant_of__isnull=True
        ).select_related("category", "brand")

        context.update(
            {
                "banners": models.Banner.objects.filter(is_active=True).order_by(
                    "order"
                ),
                "featured_products": base_products.filter(is_featured=True)[:8],
                "best_sellers": base_products.filter(is_best_seller=True)[:8],
                "new_products": base_products.filter(is_new=True)[:8],
                "special_offers": base_products.filter(is_special_offer=True)[:8],
                "categories": models.Category.objects.filter(parent=None),
                "brands": models.Brand.objects.all()[:10],
            }
        )
        return context


class FeaturedProductList(generic.ListView):
    model = models.Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return models.Product.objects.filter(is_featured=True, variant_of__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Featured Products"
        return context


class NewProductList(generic.ListView):
    model = models.Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return models.Product.objects.filter(
            is_new=True, variant_of__isnull=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "New Arrivals"
        return context


class SpecialOfferList(generic.ListView):
    model = models.Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return models.Product.objects.filter(
            is_special_offer=True, variant_of__isnull=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Special Offers"
        return context


class CategoryDetail(generic.DetailView):
    model = models.Category
    context_object_name = "category"
    template_name = "category_detail.html"

    def get_object(self):
        category_path = self.kwargs.get("category_path", "").rstrip("/")
        parent = None
        cat = None

        for slug in category_path.split("/"):
            cat = get_object_or_404(models.Category, slug=slug, parent=parent)
            parent = cat

        return cat

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["request"] = self.request
        category = self.object

        # breadcrumb
        breadcrumb = []
        parent = category
        while parent:
            breadcrumb.insert(0, parent)
            parent = parent.parent
        ctx["breadcrumb"] = breadcrumb

        subcategories = category.subcategories.all()
        ctx["subcategories"] = subcategories

        allowed_categories = [category] + category.get_descendants()
        products_qs = (
            models.Product.objects.filter(
                category__in=allowed_categories, variant_of=None
            )
            .select_related("brand", "category")
            .prefetch_related("images", "attributes__attribute")
        )

        filters = {}
        for key, values in self.request.GET.lists():
            if key not in ["order_by", "order"]:
                values = [v for v in values if v]
                if values:
                    filters[key] = values

        order_by_attr = self.request.GET.get("order_by")
        order_direction = self.request.GET.get("order", "asc")

        products_qs = models.Product.filter_and_sort(
            products_qs,
            filters=filters,
            order_by_attr=order_by_attr,
            order=order_direction,
        )

        attribute_options = models.Product.get_attributes_options(products_qs)
        for attr_name, options in attribute_options.items():
            options = [
                (
                    [opt, True]
                    if attr_name in filters and opt in filters[attr_name]
                    else [opt, False]
                )
                for opt in options
            ]
            attribute_options[attr_name] = options

        ctx["products"] = products_qs
        ctx["attribute_options"] = attribute_options
        ctx["order_direction"] = order_direction
        ctx["order_by_attr"] = order_by_attr

        return ctx


class ProductDetail(generic.DetailView):
    model = models.Product
    template_name = "product_detail.html"

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.object

        variants = list(product.variants.prefetch_related("attributes__attribute"))
        variants = [product] + variants
        ctx["variants"] = variants
        ctx["attributes"] = product.attributes.select_related("attribute").all()
        ctx["reviews"] = product.reviews.select_related("user").all()
        ctx["avg_rating"] = product.avg_rating
        ctx["form_review"] = forms.ProductReview()
        ctx["images"] = product.images.all()
        ctx['add_to_cart_form'] = orders_form.AddToCartProduct()

        breadcrumb = [product]
        parent = product.category
        while parent:
            breadcrumb.insert(0, parent)
            parent = parent.parent
        ctx["breadcrumb"] = breadcrumb

        return ctx

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = forms.ProductReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect(product.get_absolute_url())
        ctx = self.get_context_data()
        ctx["form_review"] = form
        return self.render_to_response(ctx)


class ReviewUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.ProductReview
    model = models.ProductReview
    template_name = "product_review.html"

    def get_success_url(self):
        return self.object.product.get_absolute_url()
