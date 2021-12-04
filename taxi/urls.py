
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import main.views as main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.main, name='main'),
    path('products/', include('main.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('order/', include('orderapp.urls', namespace='order')),
    path('contacts/', main.contacts, name='contacts')
]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
