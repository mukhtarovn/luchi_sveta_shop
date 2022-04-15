import json
import os
import random
from datetime import datetime


from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView

from basketapp.models import Basket
from main.models import Product, ProductCategory, ProductType


def main(request):
    title = 'лучи света'
    products = Product.objects.exclude(category__name='Technical'). \
        exclude(category__name='Voltega').exclude(category__name='Outdoor').filter(quantity=True)
    random_products = random.sample(list(products), 3)
    content = {
        'title': title,
        'products': products,
        "types": ProductType.objects.all(),
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
    try:
        _products = Product.objects.filter(sale_price__isnull = False) #exclude(category__name='Technical').exclude(category__name='Outdoor'). \
            #exclude(category__name='Voltega').exclude(quantity=0)
    except:
        _products = Product.objects.all()
    return random.sample(list(_products), 1)[0]

def get_product_by_price(pk=None):
    products = Product.objects.filter(category__pk=pk).order_by('price')
    return products

def get_same_products(hot_product):
    _same_products = Product.objects.filter(category=hot_product.category).exclude(quantity=0).\
        exclude(pk=hot_product.pk)
    random_prod = random.sample(list(_same_products), 3)
    return random_prod

def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()
    type_menu = ProductType.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().exclude(quantity=0)
            category = {'pk':0, 'name':'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).exclude(quantity=0)

        paginator = Paginator(products, 21)
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
            'type_menu': type_menu,
            'title': title,
            'category': category,
            'products': product_paginator, #products,
            'basket': get_basket(request.user),
            'last_page': last_page,
            'first_page': first_page,
            'by_price': get_product_by_price(pk)
            }
        return render(request, 'main/products_list.html', content)

    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)
    content = {
        'links_menu': links_menu,
        'type_menu': type_menu,
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
        'type_menu': ProductType.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'same_product': get_same_products(product_item)
    }
    return render(request, 'main/product.html', content)

def search_result(request):
    query = request.GET.get ('search')
    products_item = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query)
                                        |Q(article__icontains= query)).exclude(quantity=0)

    content = {
        'title': 'Поиск',
        'result': products_item
    }
    return render(request, 'main/search_results.html', content)


def info(request):
    title = 'Информация'
    content = {
        'title': title,
    }
    return render (request, 'main/info.html', content)

def by_price(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    if pk == 0:
        products = Product.objects.all().exclude(quantity=0).order_by('price')
        category = {'pk':0, 'name':'все'}
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category__pk=pk).exclude(quantity=0).order_by('price')

    content = {
            'links_menu': links_menu,
            'type_menu': ProductType.objects.all(),
            'title': title,
            'category': category,
            'products': products,
            'basket': get_basket(request.user),
            }
    return render(request, 'main/products_list.html', content)


def types(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    types = get_object_or_404(ProductType, pk=pk)
    products = Product.objects.filter(type__pk=pk).exclude(quantity=0)


    content = {
            'links_menu': links_menu,
            'type_menu': ProductType.objects.all(),
            'title': title,
            'types': types,
            'products': products,
            'basket': get_basket(request.user),
            }
    return render(request, 'main/types.html', content)