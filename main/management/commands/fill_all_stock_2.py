import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from main.models import ProductCategory, Product, ProductType, ProductType_2

FILE_PATH = os.path.join(settings.BASE_DIR, 'main/json')

def load_from_json(file_name):
    with open(os.path.join(FILE_PATH, file_name + '.json')) as json_file:
        return json.load(json_file)

class Command(BaseCommand):

    def handle(self, *args, **options):
        # categories = load_from_json("categories")
        # ProductCategory.objects.all().delete()
        # for cat in categories:
        #     ProductCategory.objects.create(**cat)
        #
        # types = load_from_json("type")
        # ProductType.objects.all().delete()
        # for type in types:
        #     ProductType.objects.create(**type)
        #
        # types_2 = load_from_json("type_2")
        # ProductType_2.objects.all().delete()
        # for type_2 in types_2:
        #     type_name = type_2["parent_type"]
        #     _type = ProductType.objects.get(name=type_name)
        #     type_2["parent_type"] = _type
        #     ProductType_2.objects.create(**type_2)

        products = load_from_json("vam_svet_2")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = int (prod['price'])
                _quantity = int (prod['quantity'])
                if prod['sale_price']:
                    _sale_price = _price
                    _price = prod['sale_price']
                    if _price < _sale_price:
                        prod["price"] = _sale_price
                        prod['sale_price'] = int (_price)

            except KeyError:
                _quantity = 0
            Product.objects.filter(article=_article).update(price=_price, quantity=_quantity, sale_price=_sale_price)

#ShopUser.objects.all().delete()
    #ShopUser.objects.create_superuser(username='nariman', password='sarvan030511', age=30, first_name='Нариман', )