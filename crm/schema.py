import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter

# ----------------------------
# Node Types
# ----------------------------
class DummyMutation(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, info):
        return DummyMutation(ok=True)

class Mutation(graphene.ObjectType):
    dummy = DummyMutation.Field()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(lambda: CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node, )

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node, )

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node, )

# ----------------------------
# Query with filters
# ----------------------------
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)



# ----------------------------
# Mutation placeholder
# ----------------------------


