import random
from io import BytesIO
from django.core.files import File
from faker import Faker
from shop.models import (
    Category,
    Brand,
    Product,
    Attribute,
    ProductAttribute,
    ProductImage,
)

fake = Faker()

# ------------------------------
# 1. دسته‌بندی‌ها
# ------------------------------
mobile_cat, _ = Category.objects.get_or_create(name="Mobile", slug="mobile")
laptop_cat, _ = Category.objects.get_or_create(name="Laptop", slug="laptop")
digital_cat, _ = Category.objects.get_or_create(name="Digital", slug="digital")

# ------------------------------
# 2. برندها
# ------------------------------
brands = [
    "Apple",
    "Samsung",
    "Xiaomi",
    "Lenovo",
    "Asus",
    "HP",
    "Canon",
    "Sony",
    "Logitech",
]
brand_objs = []
for b in brands:
    brand_obj, _ = Brand.objects.get_or_create(name=b)
    brand_objs.append(brand_obj)

# ------------------------------
# 3. Attributes
# ------------------------------
mobile_attrs = ["RAM", "Storage", "Battery", "Color", "Price"]
laptop_attrs = ["RAM", "Storage", "Weight", "Processor", "Color", "Price"]
digital_attrs = ["Type", "Warranty", "Color", "Price"]

for attr_name in mobile_attrs:
    Attribute.objects.get_or_create(name=attr_name, category=mobile_cat)
for attr_name in laptop_attrs:
    Attribute.objects.get_or_create(name=attr_name, category=laptop_cat)
for attr_name in digital_attrs:
    Attribute.objects.get_or_create(name=attr_name, category=digital_cat)

# ------------------------------
# 4. ایجاد محصولات
# ------------------------------
categories = [mobile_cat, laptop_cat, digital_cat]

for i in range(30):
    category = random.choice(categories)
    brand = random.choice(brand_objs)
    name = f"{brand.name} {fake.word().capitalize()} {i+1}"
    slug = name.lower().replace(" ", "-")

    # قیمت بر اساس دسته
    if category == mobile_cat:
        price = random.randint(300, 1500) * 10
    elif category == laptop_cat:
        price = random.randint(1000, 4000) * 10
    else:  # Digital
        price = random.randint(50, 500) * 10

    product = Product.objects.create(
        name=name,
        slug=slug,
        category=category,
        brand=brand,
        price=price,
        desc=fake.text(max_nb_chars=250),
    )

    # ------------------------------
    # 5. اضافه کردن attributes
    # ------------------------------
    if category == mobile_cat:
        attrs = mobile_attrs
    elif category == laptop_cat:
        attrs = laptop_attrs
    else:
        attrs = digital_attrs

    for attr_name in attrs:
        attribute = Attribute.objects.get(name=attr_name, category=category)
        if attr_name == "RAM":
            value = random.choice(["4GB", "6GB", "8GB", "12GB", "16GB"])
        elif attr_name == "Storage":
            value = random.choice(["64GB", "128GB", "256GB", "512GB", "1TB"])
        elif attr_name == "Battery":
            value = random.choice(["3000mAh", "3500mAh", "4000mAh", "5000mAh"])
        elif attr_name == "Color":
            value = random.choice(["Black", "White", "Blue", "Red", "Gray", "Silver"])
        elif attr_name == "Weight":
            value = random.choice(["1kg", "1.3kg", "1.5kg", "2kg"])
        elif attr_name == "Processor":
            value = random.choice(
                ["i3", "i5", "i7", "i9", "Ryzen 3", "Ryzen 5", "Ryzen 7"]
            )
        elif attr_name == "Type":
            value = random.choice(
                ["Headphones", "Mouse", "Keyboard", "Camera", "Speaker"]
            )
        elif attr_name == "Warranty":
            value = random.choice(["6 months", "1 year", "2 years"])
        elif attr_name == "Price":
            value = str(product.price)
        else:
            value = fake.word()

        ProductAttribute.objects.create(
            product=product,
            attribute=attribute,
            value=value,
        )

    # ------------------------------
    # 6. اضافه کردن تصاویر با fallback امن
    # ------------------------------
    for j in range(1, 4):
        width, height = 400, 400
        url = f"http://picsum.photos/seed/{slug}-{j}/{width}/{height}"  # http

        img_file = None
        try:
            import requests

            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img_file = File(BytesIO(response.content), name=f"{slug}_{j}.jpg")
        except Exception:
            pass  # اینترنت نبود یا requests نصب نبود -> عکس اضافه نمی‌کنیم

        if img_file:
            ProductImage.objects.create(
                product=product,
                img=img_file,
                is_main=(j == 1),
            )

print(
    "✅ complete"
)
