# alx_backend_graphql_crm/schema.py
import graphene
from crm.schema import CRMQuery

class Query(CRMQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query)
