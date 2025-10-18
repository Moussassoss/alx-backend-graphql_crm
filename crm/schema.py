import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.validators import RegexValidator
from django.db import transaction
from django.db.utils import IntegrityError
from graphene import Field, List, String, Float, Int

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
# -----------------------------
# Query
# -----------------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.prefetch_related('products').all()


# -----------------------------
# CreateCustomer
# -----------------------------
class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    customer = Field(CustomerType)
    message = String()

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
