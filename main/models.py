from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    article = models.CharField(verbose_name='имя продукта', max_length= 128, blank=True, null=True)
    name = models.CharField(verbose_name='имя продукта', max_length= 128)
    series = models.CharField(verbose_name='серия', max_length= 64, blank=True, null=True)
    type = models.CharField(verbose_name='тип светильника', max_length= 64, blank=True, null=True)
    type_2 = models.CharField(verbose_name='подтип', max_length= 64, blank=True, null=True)
    material = models.CharField(verbose_name='метериал', max_length= 64, blank=True, null=True)
    color = models.CharField(verbose_name='цвет', max_length= 64, blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='цена', null=True)
    lamps = models.PositiveIntegerField (verbose_name='количество ламп', null=True)
    lamps_type = models.CharField(verbose_name='цоколь', max_length=16, blank=True, null=True)
    power = models.CharField(verbose_name='мощность', max_length=16, null=True)
    length = models.CharField(verbose_name='длина', max_length=16, null=True)
    width = models.CharField(verbose_name='ширина', max_length=16, null=True)
    height = models.CharField(verbose_name='высота', max_length=16, null=True)
    diameter = models.CharField(verbose_name='диаметр', max_length=16, null=True)
    size = models.CharField(verbose_name='размер', blank=True, max_length=32, null=True)
    weight = models.CharField(verbose_name='вес', max_length=16, blank=True, null=True)
    image = models.ImageField(verbose_name='фото', upload_to='products_images', blank=True, null=True)
    image_2 = models.ImageField(verbose_name='фото-2', upload_to='products_images', blank=True, null=True)
    image_3 = models.ImageField(verbose_name='фото-3', upload_to='products_images', blank=True, null=True)
    image_4 = models.ImageField(verbose_name='фото-4', upload_to='products_images', blank=True, null=True)
    image_5 = models.ImageField(verbose_name='фото-5', upload_to='products_images', blank=True, null=True)
    short_desc = models.CharField(verbose_name='краткое описание', max_length=64, blank=True)
    descriptions = models.CharField(verbose_name='описание', max_length=128, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def get_absolute_url(self):
        return 'https://luchi-sveta.ru/products/product/' +str(self.pk)

    def __str__(self):
        return f'{self.name} ({self.category.name})'