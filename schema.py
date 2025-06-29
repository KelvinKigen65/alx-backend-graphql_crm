"""
GraphQL Schema for alx-backend-graphql_crm project
"""

import graphene


class Query(graphene.ObjectType):
    """
    Main GraphQL Query class that defines all available queries
    """
    
    # Define the hello field
    hello = graphene.String(description="A simple hello world query")
    
    def resolve_hello(self, info):
        """
        Resolver for the hello field
        Returns a greeting message
        """
        return "Hello, GraphQL!"


# Create the schema
schema = graphene.Schema(query=Query)