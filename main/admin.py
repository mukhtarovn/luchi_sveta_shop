from django.contrib import admin

from main.models import ProductCategory, Product

#admin.site.register(ProductCategory)
#admin.site.register(Product)

@admin.register(ProductCategory)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ('name',)
    search_fields = ['name']
    list_filter = (
        'name',)
    view_on_site = True

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'category', 'price', 'quantity']
    ordering = ('category',)
    search_fields = ['article', 'name',]
    list_filter = (
        'category',)




