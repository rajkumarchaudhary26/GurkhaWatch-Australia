from django.contrib import admin
from .models import ProductSlider
# Register your models here.


class ProductSliderAdmin(admin.ModelAdmin):
    list_display = [
        'slider_product_name', 'slider_product_price', 'slider_product_discount_percent',
    ]


admin.site.register(ProductSlider, ProductSliderAdmin)
