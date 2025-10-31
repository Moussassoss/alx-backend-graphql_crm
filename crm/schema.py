import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from django.core.validators import RegexValidator
from django.db import IntegrityError, transaction
from .models import Customer, Product, Order
from crm.models import Product
from .filters import CustomerFilter, ProductFilter, OrderFilter

# -----------------------------
# GraphQL Types
# -----------------------------

# Relay-enabled types with filtering
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        filterset_class = CustomerFilter

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        filterset_class = ProductFilter

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)
        filterset_class = OrderFilter

# -----------------------------
# Queries
# -----------------------------
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode, order_by=graphene.String())
    all_orders = DjangoFilterConnectionField(OrderNode, order_by=graphene.String())

    def resolve_all_products(root, info, order_by=None, **kwargs):
        qs = Product.objects.all()
        if order_by:
            qs = qs.order_by(order_by)
        return qs

    def resolve_all_orders(root, info, order_by=None, **kwargs):
        qs = Order.objects.prefetch_related('products').all()
        if order_by:
            qs = qs.order_by(order_by)
        return qs

# -----------------------------
# Mutations
# -----------------------------

# ----------- CreateCustomer -----------
class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    customer = graphene.Field(CustomerNode)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        phone_validator = RegexValidator(
            regex=r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$',
            message="Phone must be in +1234567890 or 123-456-7890 format."
        )
        try:
            if input.phone:
                phone_validator(input.phone)
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone
            )
            return CreateCustomer(customer=customer, message="Customer created successfully.")
        except IntegrityError:
            return CreateCustomer(customer=None, message="Email already exists.")
        except Exception as e:
            return CreateCustomer(customer=None, message=str(e))

# ----------- BulkCreateCustomers -----------
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CreateCustomerInput, required=True)

    customers = graphene.List(CustomerNode)
    errors = graphene.List(graphene.String)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        created = []
        errors = []

        for c in input:
            try:
                if c.phone:
                    RegexValidator(
                        regex=r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$',
                        message="Phone must be in +1234567890 or 123-456-7890 format."
                    )(c.phone)
                customer = Customer.objects.create(
                    name=c.name,
                    email=c.email,
                    phone=c.phone
                )
                created.append(customer)
            except IntegrityError:
                errors.append(f"Email '{c.email}' already exists.")
            except Exception as e:
                errors.append(f"{c.email if c.email else c.name}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)

# ----------- CreateProduct -----------
class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=False, default_value=0)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(ProductNode)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        if input.price <= 0:
            return CreateProduct(product=None, message="Price must be positive.")
        if input.stock < 0:
            return CreateProduct(product=None, message="Stock cannot be negative.")
        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock
        )
        return CreateProduct(product=product, message="Product created successfully.")

# ----------- CreateOrder -----------
class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.String(required=False)  # Optional

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)

    order = graphene.Field(OrderNode)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(order=None, message="Customer not found.")

        if not input.product_ids:
            return CreateOrder(order=None, message="At least one product must be selected.")

        products = Product.objects.filter(pk__in=input.product_ids)
        if products.count() != len(input.product_ids):
            return CreateOrder(order=None, message="Some products not found.")

        total_amount = sum([p.price for p in products])
        order = Order.objects.create(customer=customer, total_amount=total_amount)
        order.products.set(products)
        order.save()

        return CreateOrder(order=order, message="Order created successfully.")

# ----------- UpdateLowStockProducts -----------
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    updated_products = graphene.List(ProductNode)
    message = graphene.String()

    @staticmethod
    def mutate(root, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(product)

        msg = f"{len(updated)} products restocked successfully." if updated else "No products needed restocking."
        return UpdateLowStockProducts(updated_products=updated, message=msg)

# -----------------------------
# Root Mutation
# -----------------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

