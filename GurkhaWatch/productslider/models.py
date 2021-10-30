from django.db import models
from shop.models import Product
from tinymce.models import HTMLField
# Create your models here.


class ProductSlider(models.Model):
    slider_product_name = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='slider_product_name')
    slider_description = HTMLField()
    slider_product_price = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='slider_product_price')
    # default = 0, so that it doesn't throw 'NoneType' error when null
    slider_product_discount_percent = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='slider_product_discount_percent')
    slider_product_image = models.ImageField(
        upload_to='photos/product_slider', )

    def __unicode__(self):
        return self.slider_product_name
