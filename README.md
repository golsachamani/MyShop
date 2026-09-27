# MyShop

A Django-based e-commerce project inspired by modern online shopping platforms such as Digikala.

MyShop provides a server-rendered shopping experience with product catalog management, hierarchical categories, product attributes, reviews, user authentication, shopping cart functionality, and order/payment data models.

> **Project status:** The current project focuses on the web-based Django implementation. Automated tests and the API/DRF layer are planned for future development.

## Features

### 👤 User Authentication

- User registration
- Login / logout
- Profile editing
- Password change
- Authentication-protected pages
- Authentication-aware navigation

### 🛍️ Product Catalog

- Products and brands
- Multiple product images
- Product descriptions and prices
- Stock quantities and stock status
- Featured products
- Best sellers
- New arrivals
- Special offers
- Product variants
- Dynamic product attributes/specifications

### 📂 Hierarchical Categories

Categories support parent/child relationships, subcategory navigation, breadcrumbs, and category paths.

Category pages support:

- Subcategory navigation
- Products from the selected category and descendants
- Attribute-based filtering
- Sorting by attributes
- Ascending/descending ordering
- Empty-state handling

### 🔎 Filtering & Sorting

Product attributes are used for dynamic filtering. Numeric attributes such as RAM, storage, weight, and price are converted to numeric values before sorting.

### ⭐ Reviews & Ratings

Authenticated users can submit product reviews with a rating from 1 to 5 and an optional comment.

The system includes:

- Average product rating
- Review list
- Reviewer information
- Review dates
- One review per user/product through a database constraint
- Review editing through the product interface

### 🖼️ Product Images & Variants

Products can have multiple images and a main image. Product pages provide an image gallery with client-side thumbnail switching.

Products also support self-referencing variants, which are displayed and selectable in the product detail interface.

### 🛒 Shopping Cart

The active cart is represented by an `Order` with status `none`.

Users can:

- Add products
- Specify quantity
- Increase quantity for an existing cart item
- View cart/order information
- Remove cart items
- Confirm deletion before removing an item

### 📦 Orders

Orders contain a user, status, payment date, items, and a calculated total price.

Supported statuses include:

```text
none
canceled
paid
done
```

Users see their own orders in the order list.

### 💳 Payment Model

The project includes a payment data model with states such as `none`, `init`, `processing`, `rejected`, and `completed`, along with transaction/reference information and gateway data.

A complete payment-gateway/checkout flow is not currently presented as a finished feature.

### 🏷️ Homepage

The homepage includes sections for:

- Featured products
- Best sellers
- New arrivals
- Special offers
- Active banners
- Categories
- Brands

### 🖼️ Banners

Banners can target a product, category, or external URL and can be enabled/ordered from the data model.

## 🧱 Project Architecture

```text
MyShop/
├── accounts/   # Authentication and user-related pages
├── shop/       # Catalog, categories, products and reviews
├── orders/     # Cart, orders and payment data
├── config/     # Django project configuration
├── static/     # CSS and JavaScript assets
├── manage.py
└── seed_products.py
```

### `accounts`

Handles registration, login, logout, profile editing, and password management.

### `shop`

Handles categories, brands, products, images, attributes, variants, reviews, banners, and catalog pages.

### `orders`

Handles orders, order items, cart operations, and payment data.

### `config`

Contains the main Django settings, root URLs, ASGI/WSGI configuration, and base template.

### `static`

Contains custom CSS and JavaScript assets for the frontend.

## 🎨 Frontend

The project uses Django Templates, Bootstrap 5.3.2, HTML5, CSS3, and JavaScript.

The base layout is defined in `config/templates/base.html` and is reused through Django template inheritance.

Custom frontend assets cover:

- Brand/theme styling
- Categories
- Category detail pages
- Mega menu
- Product detail pages
- Category interactions
- Product detail interactions

The interface includes a responsive navigation bar, category mega menu, breadcrumbs, responsive product grids, and authentication-aware navigation.

## 🛡️ Django & Security Patterns

The project uses Django's built-in authentication and class-based views, including:

- `LoginRequiredMixin`
- `LoginView`
- `CreateView`
- `UpdateView`
- `DeleteView`
- `ListView`
- `DetailView`
- `TemplateView`
- `PasswordChangeView`

It also uses Django CSRF protection on POST forms and restricts the order list to the authenticated user's orders.

## ⚡ ORM & Querying

The project uses Django ORM features including:

```python
filter()
select_related()
prefetch_related()
aggregate()
annotate()
order_by()
```

Product attribute sorting uses ORM expressions such as `Cast`, `Coalesce`, and `F` expressions.

## 🗃️ Main Data Model

```text
Category
├── Subcategories
├── Products
│   ├── ProductImage
│   ├── ProductAttribute
│   ├── ProductReview
│   └── Product variants
└── Attributes

Brand
└── Products

Order
├── OrderItem
└── Payment

User
├── Orders
└── ProductReviews
```

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd MyShop
```

### 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

## 🌱 Seed Data

The repository contains `seed_products.py` for product seed data.

## 🧪 Testing

Automated tests have not been implemented yet. Testing is planned as a future part of the project.

Planned test areas include:

- Models
- Authentication
- Product/catalog behavior
- Category filtering and sorting
- Reviews
- Cart
- Orders
- Ownership and permission behavior

## 🚧 Roadmap

Planned improvements include:

- Automated test suite
- Completing the API/DRF layer
- Product search backend
- Complete checkout flow
- Payment gateway integration
- Improved cart/variant integration
- Additional order management functionality
- Further frontend refinements
- Production deployment configuration

## 📌 Current Scope

The current web application covers the main catalog and shopping flow:

```text
Authentication
      ↓
Homepage
      ↓
Categories
      ↓
Filtering / Sorting
      ↓
Product Detail
      ↓
Reviews
      ↓
Shopping Cart
      ↓
Orders
```

The project is being developed incrementally, with testing, API functionality, checkout, and payment integration planned for later stages.

## 📚 Technologies

| Technology | Usage |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django ORM | Database interaction |
| Django Templates | Server-side rendering |
| Bootstrap 5.3.2 | Responsive UI |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side interactions |

## 📄 License

No license has been specified for this project yet.
