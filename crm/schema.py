import graphene

class CustomerType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

# Dummy data
CUSTOMERS = [
    {"id": "1", "name": "Alice", "email": "alice@example.com"},
    {"id": "2", "name": "Bob", "email": "bob@example.com"},
]

class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return [CustomerType(**customer) for customer in CUSTOMERS]
