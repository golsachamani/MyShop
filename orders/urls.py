from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderList.as_view(), name="order_list"),
    path("add_cart/<int:pk>/", views.AddToCart.as_view(), name="add_to_cart"),
    path('remove_item/<int:pk>/',views.RemoveCart.as_view(),name= 'remove_item'),

]
