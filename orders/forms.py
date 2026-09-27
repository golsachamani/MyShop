from django import forms
from . import models
class AddToCartProduct(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields= ['quantity']