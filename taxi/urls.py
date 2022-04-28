
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

import main.views as main
if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.main, name='main'),
    path('products/', include('main.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('order/', include('orderapp.urls', namespace='order')),
    path('contacts/', main.contacts, name='contacts'),
    #path('admin/', include('adminapp.urls', namespace='admin'))

]


if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [re_path(r'^__debug__', include(debug_toolbar.urls))]
