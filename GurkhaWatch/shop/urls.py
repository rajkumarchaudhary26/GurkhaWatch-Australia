from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    # to tell program not to consider search a category
    # path('category/<slug:category_slug>/', views.shop, name='products_by_category'),
    # path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('search/', views.search, name='search'),
    
]
