import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Category, Product


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"
        filter_fields = ['name', 'slug']
        interfaces = (relay.Node, )


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__slug': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)