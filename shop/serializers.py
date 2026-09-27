from . import models
from rest_framework import serializers

class Product(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
        
class Category(serializers.ModelSerializer):
   
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'slug', 'subcategories']
    
    def get_subcategories(self, obj):
        # بازگشتی برای تمام سطوح
        return Category(
            obj.subcategories.filter(root_menu_order__gt=0), 
            many=True
        ).data if hasattr(obj, 'subcategories') else []