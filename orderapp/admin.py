from django.contrib import admin

# Register your models here.
from django.contrib import admin

from orderapp.models import Order

admin.site.register(Order)