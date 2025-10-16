import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

# Seed Customers
Customer.objects.bulk_create([
    Customer(name="Alice", email="alice@example.com", phone="+1234567890"),
    Customer(name="Bob", email="bob@example.com"),
    Customer(name="Carol", email="carol@example.com"),
])

# Seed Products
Product.objects.bulk_create([
    Product(name="Laptop", price=999.99, stock=10),
    Product(name="Mouse", price=25.50, stock=50),
    Product(name="Keyboard", price=45.00, stock=20),
])

print("✅ Database seeded successfully")
