import graphene
from crm.schema import CRMQuery  # make sure this import matches your crm/schema.py location

class Query(CRMQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
