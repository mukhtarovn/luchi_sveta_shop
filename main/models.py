from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'
    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    article = models.CharField(verbose_name='артикул', max_length= 128, blank=True, null=True)
    name = models.CharField(verbose_name='имя продукта', max_length= 256, null=True)
    series = models.CharField(verbose_name='серия', max_length= 128, blank=True, null=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    type_2 = models.CharField(verbose_name='подтип', max_length= 64, blank=True, null=True)
    material = models.CharField(verbose_name='метериал', max_length= 256, blank=True, null=True)
    color = models.CharField(verbose_name='цвет', max_length= 64, blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='цена', null=True)
    sale_price =models.PositiveIntegerField(verbose_name='цена cо скидкой', null=True, blank=True)
    lamps = models.CharField (verbose_name='количество ламп', max_length=32, null=True, blank=True)
    lamps_type = models.CharField(verbose_name='цоколь', max_length=32, blank=True, null=True)
    power = models.CharField(verbose_name='мощность', max_length=32, null=True, blank=True)
    length = models.CharField(verbose_name='длина', max_length=32, null=True, blank=True)
    width = models.CharField(verbose_name='ширина', max_length=32, null=True, blank=True)
    height = models.CharField(verbose_name='высота', max_length=32, null=True, blank=True)
    diameter = models.CharField(verbose_name='диаметр', max_length=32, null=True, blank=True)
    size = models.CharField(verbose_name='размер', blank=True, max_length=64, null=True)
    weight = models.CharField(verbose_name='вес', max_length=32, blank=True, null=True)
    short_desc = models.CharField (verbose_name='краткое описание', max_length=64, blank=True)
    style = models.CharField (verbose_name='стиль', max_length=128, blank=True, null=True)
    descriptions = models.CharField(verbose_name='описание', max_length=2048, blank=True, null=True)
    quantity = models.PositiveIntegerField (verbose_name='количество на складе', default=0)
    image = models.ImageField(verbose_name='фото', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_2 = models.ImageField(verbose_name='фото-2', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_3 = models.ImageField(verbose_name='фото-3', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_4 = models.ImageField(verbose_name='фото-4', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_5 = models.ImageField(verbose_name='фото-5', upload_to='products_images', blank=True, null=True, max_length=200)


    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def get_absolute_url(self):
        return 'https://luchi-sveta.ru/products/product/' +str(self.pk)

    def __str__(self):
        return f'{self.name} ({self.category.name})'