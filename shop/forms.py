from django import forms
from . import models

class ProductReview(forms.ModelForm):
    class Meta:
        model = models.ProductReview
        fields = ['rating',  'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
