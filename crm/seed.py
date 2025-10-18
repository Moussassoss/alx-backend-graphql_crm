from .models import Customer, Product
customers = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
]
for c in customers:
    Customer.objects.get_or_create(email=c["email"], defaults=c)

products = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Mouse", "price": 49.99, "stock": 50},
]
for p in products:
    Product.objects.get_or_create(name=p["name"], defaults=p)
