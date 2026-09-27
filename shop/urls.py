from django.urls import path
from . import views
from . import views_api

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path(
        "product/<path:category_path>/<slug:product_slug>/",
        views.ProductDetail.as_view(),
        name="product_detail",
    ),
    path(
        "category/<path:category_path>/",
        views.CategoryDetail.as_view(),
        name="category_detail",
    ),
    path("comment/<int:pk>/", views.ReviewUpdate.as_view(), name="review_product"),
    path("featured/", views.FeaturedProductList.as_view(), name="featured_list"),
    path("new/", views.NewProductList.as_view(), name="new_list"),
    path(
        "special-offers/", views.SpecialOfferList.as_view(), name="special_offer_list"
    ),
]

urlpatterns += [
    path(
        "api/product/<path:category_path>/<slug:product_slug>/",
        views_api.ProductDetail.as_view(),
        name="api_product_detail",
    ),
    path(
        "api/category/<path:category_path>/",
        views_api.CategoryDetail.as_view(),
        name="api_category_detail",
    ),
    path("api/new/", views_api.NewProductList.as_view(), name="api_new_product"),
    path(
        "api/special-offers/",
        views_api.SpecialOfferList.as_view(),
        name="api_special_offer_list",
    ),
    path(
        "api/featured/",
        views_api.FeaturedProductList.as_view(),
        name="api_featured_list",
    ),
]
