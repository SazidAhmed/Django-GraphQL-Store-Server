import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

#import image lib
from io import BytesIO
from PIL import Image
from django.core.files import File

#import model
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
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__slug': ['exact'],
        }
        interfaces = (relay.Node, )

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image
    
    def resolve_thumbnail(self, info):
        if self.thumbnail:
            self.thumbnail = info.context.build_absolute_uri(self.thumbnail.url)
            return self.thumbnail
        else:
            if self.image:
                self.thumbnail = info.context.build_absolute_uri(self.image)
                return self.thumbnail
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
        


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)