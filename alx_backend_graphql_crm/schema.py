import graphene
import crm.schema

class Query(crm.schema.Query, graphene.ObjectType):
    # Combine all app-level queries here
    pass

schema = graphene.Schema(query=Query)
