from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products', )
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name
    # display manytomany field in the django admin panel    
    def get_category(self):
        return ", ".join([str(p) for p in self.category.all()])
    def __unicode__(self):
        return "{0}".format(self.product_name)