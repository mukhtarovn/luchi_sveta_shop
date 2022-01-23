from django.contrib import admin

# Register your models here.
from django.contrib import admin

from orderapp.models import Order

#admin.site.register(Order)
@admin.register(Order)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'user', 'status']
    ordering = ('created',)
    search_fields = ['created', 'status']
    list_filter = (
        ('status'),)