import json
import os
import random
from datetime import datetime


from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Prefetch
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView

from basketapp.models import Basket
from main.models import Product, ProductCategory, ProductType, ProductType_2


def main(request):
    title = 'лучи света - интернет магазин'
    products = Product.objects.exclude(category__name='Technical'). \
        exclude(category__name='Voltega').exclude(category__name='Outdoor').filter(quantity=True).select_related('category')
    random_products = random.sample(list(products), 3)
    content = {
        'title': title,
        'products': products,
        "types": ProductType.objects.all(),
        "type2": ProductType_2.objects.all(),
        'random_products': random_products,
        'basket': get_basket(request.user),
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

def products(request, pk=None, page=1, *args, **kwargs):
    title = 'лучи света: каталог, светильники'
    links_menu = ProductCategory.objects.all()
    type_menu = ProductType.objects.all()
    type2_menu = ProductType_2.objects.all().select_related('parent_type')


    if pk is not None:
        sort = request.GET.getlist('sort')
        color = ""
        price_min = 0
        price_max = 1000000
        style = ""
        material = ""
        search = ""

        if pk == 0:
            products = Product.objects.all().order_by(*sort).exclude(quantity=0).select_related('category')
            if request.GET.get('color'):
                color = request.GET.get('color')
                products = products.filter (Q (color__iregex=color))
            if request.GET.get('search'):
                search = request.GET.get('search')
                products = products.filter(Q(name__icontains=search) | Q(category__name__icontains=search)
                                        |Q(article__icontains= search))
            if request.GET.get('style'):
                style = request.GET.get('style')
                products = products.filter(style=style)
            if request.GET.get('material'):
                material = request.GET.get('material')
                products = products.filter(material=material)
            if request.GET.get('price_min'):
                price_min = request.GET.get('price_min')
            if request.GET.get ('price_max'):
                price_max = request.GET.get ('price_max')
            products=products.filter(price__range=(price_min, price_max))
            category = {'pk':0, 'name':'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).exclude(quantity=0).order_by(*sort).select_related('category')
            if request.GET.get('color'):
                color=request.GET.get('color')
                products = products.filter (Q (color__iregex=color))
            if request.GET.get('style'):
                style = request.GET.get('style')
                products = products.filter (Q (style__iregex=style))
            if request.GET.get('material'):
                material = request.GET.get('material')
                products = products.filter(material=material)
            if request.GET.get ('price_min'):
                price_min = request.GET.get ('price_min')
            if request.GET.get ('price_max'):
                price_max = request.GET.get ('price_max')
            products=products.filter(price__range=(price_min, price_max))

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
            'type2_menu': type2_menu,
            'title': title,
            'category': category,
            'products': product_paginator,
            'basket': get_basket(request.user),
            'last_page': last_page,
            'first_page': first_page,
            'q': f'?price_min={price_min}&price_max={price_max}&color={color}&style={style}&material={material}&search={search}'
            }
        return render(request, 'main/products_list.html', content)

    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)
    content = {
        'links_menu': links_menu,
        'type_menu': type_menu,
        'type2_menu': type2_menu,
        'title': title,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_product': same_product,
    }
    return render(request, 'main/products.html', content)

def contacts(request):
    title = 'Лучи света: контакты, о компании'
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
    type2_menu = ProductType_2.objects.all().select_related('parent_type')
    title = product_item.name
    content = {
        'title': title,
        'basket': get_basket(request.user),
        'links_menu': ProductCategory.objects.all(),
        'type_menu': ProductType.objects.all(),
        'type2_menu': type2_menu,
        'product': get_object_or_404(Product, pk=pk),
        'same_product': get_same_products(product_item)
    }
    return render(request, 'main/product.html', content)

def search_result(request):
    query = request.GET.get ('search')
    products_item = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query)
                                        |Q(article__icontains= query)).exclude(quantity=0)

    content = {
        'title': 'Лучи света: Поиск',
        'result': products_item
    }
    return render(request, 'main/search_results.html', content)

def info(request):
    title = 'Лучи света: Информация/контакты'
    content = {
        'title': title,
    }
    return render (request, 'main/info.html', content)


def types(request, pk=None, page=1, *args, **kwargs):
    sort = request.GET.getlist('sort')
    links_menu = ProductCategory.objects.all()
    type2_menu = ProductType_2.objects.all().select_related('parent_type')
    color = ""
    style = ""
    material = ""
    search = ""
    price_min = 0
    price_max = 1000000
    sort = request.GET.getlist('sort')

    if pk < 2000:
        products = Product.objects.filter(type_id=pk).exclude(quantity=0).order_by(*sort).select_related('category')
        types = get_object_or_404 (ProductType, pk=pk)

    else:
        products = Product.objects.filter(type_2=pk).exclude(quantity=0).order_by(*sort).select_related('category')
        types = get_object_or_404 (ProductType_2, pk=pk)
    title = f'Лучи света: каталог, {types.name}'
    if request.GET.get('color'):
        color=request.GET.get('color')
        products = products.filter(Q (color__iregex=color))
    if request.GET.get ('search'):
        search = request.GET.get('search')
        products = products.filter (Q (name__icontains=search) | Q (category__name__icontains=search)
                                    | Q (article__icontains=search))
    if request.GET.get('style'):
        style = request.GET.get('style')
        products = products.filter (Q(style__iregex=style))
    if request.GET.get('material'):
        material = request.GET.get('material')
        products = products.filter (Q(material__iregex=material))
    if request.GET.get('price_min'):
        price_min = request.GET.get ('price_min')
    if request.GET.get ('price_max'):
        price_max = request.GET.get ('price_max')
    products = products.filter(price__range=(price_min, price_max))
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
            'type_menu': ProductType.objects.all(),
            'type2_menu': type2_menu,
            'title': title,
            'types': types,
            'products': product_paginator,
            'last_page': last_page,
            'first_page': first_page,
            'basket': get_basket(request.user),
            'q': f'?price_min={price_min}&price_max={price_max}&color={color}&style={style}&material={material}&search={search}'
    }
    return render(request, 'main/types.html', content)

def sales(request, page=1):
    title = 'Лучи света: Скидки, Акции'
    links_menu = ProductCategory.objects.all()
    type2_menu = ProductType_2.objects.all().select_related('parent_type')
    category = {'pk': 0, 'name': 'Акиции', 'description': 'Скидки'}
    sort = request.GET.getlist ('sort')
    color = ""
    style = ""
    material = ""
    search = ""
    price_min = 0
    price_max = 1000000
    products = Product.objects.filter(sale_price__isnull=False).exclude(quantity=0).order_by(*sort).select_related('category')
    if request.GET.get('color'):
        color = request.GET.get ('color')
        products = products.filter (Q (color__iregex=color))
    if request.GET.get ('search'):
        search = request.GET.get ('search')
        products = products.filter (Q (name__icontains=search) | Q (category__name__icontains=search)
                                    | Q (article__icontains=search))
    if request.GET.get ('style'):
        style = request.GET.get ('style')
        products = products.filter (Q (style__iregex=style))
    if request.GET.get ('material'):
        material = request.GET.get ('material')
        products = products.filter (Q (material__iregex=material))
    if request.GET.get ('price_min'):
        price_min = request.GET.get('price_min')
    if request.GET.get ('price_max'):
        price_max = request.GET.get ('price_max')
    products = products.filter(price__range=(price_min, price_max))
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
            'type_menu': ProductType.objects.all(),
            'type2_menu': type2_menu,
            'title': title,
            'types': types,
            'category': category,
            'products': product_paginator,
            'last_page': last_page,
            'first_page': first_page,
            'basket': get_basket(request.user),
            'q': f'?price_min={price_min}&price_max={price_max}&color={color}&style={style}&material={material}&search={search}'
            }
    return render(request, 'main/sales.html', content)


def price_maytoni(request):
    content = {
        'title': "Прайс maytoni",
    }
    return render(request, 'main/all.yml', content)

def price_mw(request):
    content = {
        'title': "Прайс mw",
    }
    return render(request, 'main/stock_files.php.xml', content)


def price_lussole(request):
    content = {
        'title': "Прайс lussole",
    }
    return render(request, 'main/info_lussoleru_yandex.xml', content)

def price_stluce(request):
    content = {
        'title': "Прайс stluce",
    }
    return render(request, 'main/stluce_mrc.xml', content)
