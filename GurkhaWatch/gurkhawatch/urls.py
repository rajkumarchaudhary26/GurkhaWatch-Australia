"""gurkhawatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from gurkhawatch import settings
from django.contrib import admin
from django.urls import path, include
from . import views as gurkhawatch_views
from shop import views as shop_views
from carts import views as cart_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gurkhawatch_views.home, name='home'),
    path('about/', gurkhawatch_views.about, name='about'),
    path('blog/', gurkhawatch_views.blog, name='blog'),
    path('contact/', gurkhawatch_views.contact, name='contact'),
    path('shop/', shop_views.shop, name='shop'),
    path('cart/', cart_views.cart, name='cart'),
    path('add_cart/<int:product_id>/', cart_views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', cart_views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', cart_views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', cart_views.checkout, name='checkout'),
    path('product-category/<slug:category_slug>/', shop_views.shop, name='products_by_category'),
    path('product/<slug:product_slug>/', shop_views.product_detail, name='product_detail'),
    path('search/', shop_views.search, name='search'),
    path('my-account/', include('accounts.urls')),

    # path('product-category/<slug:slug>/', gurkhawatch_views.category, name='category')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "GurkhaWatch Admin"
admin.site.site_title = "GurkhaWatch Admin Portal"
admin.site.index_title = "Welcome to GurkhaWatch Portal"
