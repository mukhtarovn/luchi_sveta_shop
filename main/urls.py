
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import main.views as main

app_name = 'main'

urlpatterns = [
    path('', main.products, name='index'),
    path('category/<int:pk>/', main.products, name='category'),
    path('category/<int:pk>/<int:page>', main.products, name='page'),
    path('product/<int:pk>/', main.product, name='product')
]
