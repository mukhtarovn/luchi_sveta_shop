import json
import os
import random
from datetime import datetime


from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
from main.models import Product, ProductCategory

def main(request):
    title = 'главная'
    products = Product.objects.all()
    random_products = random.sample(list(products), 3)
    content = {
        'title': title,
        'products': products,
        'random_products': random_products,
        'basket': get_basket (request.user),
    }
    return render(request, 'main/index.html', content)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    _products = Product.objects.all()

    return random.sample(list(_products), 1)[0]

def get_same_products(hot_product):
    _same_products = Product.objects.filter(category=hot_product.category).\
        exclude(pk=hot_product.pk)[:3]
    return _same_products

def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'pk':0, 'name':'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 12)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)
        last_page = paginator.num_pages
        first_page = 1

        content = {
            'links_menu': links_menu,
            'title': title,
            'category': category,
            'products': product_paginator, #products,
            'basket': get_basket(request.user),
            'last_page': last_page,
            'first_page': first_page,
            }
        return render(request, 'main/products_list.html', content)

    hot_product = get_hot_product ()
    same_product = get_same_products (hot_product)
    content = {
        'links_menu': links_menu,
        'title': title,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_product': same_product

    }
    return render(request, 'main/products.html', content)

def contacts(request):
    title = 'Контакты'
    visit_date = datetime.now()
    locations =None
    with open(os.path.join(settings.BASE_DIR, 'main/json/contacts.json')) as json_file:
        locations = json.load(json_file)
    content = {
        'title': title,
        'visit_date': visit_date,
        'locations': locations
    }
    return render(request, 'main/contact.html', content)

def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    title = product_item.name
    content = {
        'title': title,
        'basket': get_basket(request.user),
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'same_product': get_same_products(product_item)
    }
    return render(request, 'main/product.html', content)
