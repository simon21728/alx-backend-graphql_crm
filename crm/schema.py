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
    hello = graphene.String(description="A simple hello world field")

    def resolve_hello(root, info):
        return "Hello, GraphQL!"