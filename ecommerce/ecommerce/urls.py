"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from ecomm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index.html', views.index, name='index'),
    url(r'^product.html', views.product, name='product'),
    url(r'^basket.html', views.basket, name='basket'),
    url(r'^checkout-address.html', views.checkout_address, name='checkout_address'),
    url(r'^checkout-payment.html', views.checkout_payment, name='checkout_payment'),
    url(r'^checkout-review.html', views.checkout_review, name='checkout_review'),
    url(r'^place-order.html', views.place_order, name='place_order'),
    url(r'getFail', views.get_fail),
    url(r'saveAddress', views.saveAddress),
    url(r'^$', views.index, name='index'),
    url(r'isLogged', views.is_logged, name='index'),

]

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
