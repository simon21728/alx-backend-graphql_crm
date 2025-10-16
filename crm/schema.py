import graphene
from graphene_django import DjangoObjectType
from django.db import IntegrityError
from django.utils import timezone
from .models import Customer, Product, Order

# ----------------------------
# Object Types
# ----------------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# ----------------------------
# Input Types
# ----------------------------
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(default_value=0)

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

# ----------------------------
# Mutations
# ----------------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone
            )
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except IntegrityError:
            return CreateCustomer(customer=None, message="Email already exists")
        except Exception as e:
            return CreateCustomer(customer=None, message=str(e))

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.NonNull(CustomerInput), required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, input):
        created_customers = []
        errors = []
        for data in input:
            try:
                customer = Customer.objects.create(
                    name=data.name,
                    email=data.email,
                    phone=data.phone
                )
                created_customers.append(customer)
            except IntegrityError:
                errors.append(f"Email {data.email} already exists")
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        if input.price <= 0:
            return CreateProduct(product=None, message="Price must be positive")
        if input.stock < 0:
            return CreateProduct(product=None, message="Stock cannot be negative")
        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock
        )
        return CreateProduct(product=product, message="Product created successfully")

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(order=None, message="Invalid customer ID")

        products = Product.objects.filter(pk__in=input.product_ids)
        if not products.exists():
            return CreateOrder(order=None, message="No valid products provided")

        order_date = input.order_date or timezone.now()
        order = Order.objects.create(customer=customer, order_date=order_date)
        order.products.set(products)
        order.total_amount = sum([p.price for p in products])
        order.save()

        return CreateOrder(order=order, message="Order created successfully")

# ----------------------------
# Mutation Class
# ----------------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

# ----------------------------
# Query Class
# ----------------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()
