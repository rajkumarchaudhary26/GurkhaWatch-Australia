from django.db import models
from category.models import Category
from django.urls import reverse
from tinymce.models import HTMLField
from accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # description = models.TextField(max_length=500, blank=True)
    description = HTMLField()
    price = models.IntegerField()
    # default = 0, so that it doesn't throw 'NoneType' error when null
    discount_percent = models.FloatField(default=0)
    image = models.ImageField(upload_to='photos/products', )
    stock = models.IntegerField()
    specification = models.ImageField(
        upload_to='photos/products/specifications', )
    is_available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name

    def discount(self):
        if self.discount_percent > 0:
            discounted_price = self.price - self.price * self.discount_percent / 100
            return discounted_price

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    # display manytomany field in the django admin panel

    def get_category(self):
        return ", ".join([str(p) for p in self.category.all()])

    def __unicode__(self):
        return "{0}".format(self.product_name)


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
