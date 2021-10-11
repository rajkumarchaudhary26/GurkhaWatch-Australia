from django.contrib import admin
from django.db import models
from django.db.models import fields
from .models import Product
from django import forms
from django.forms import CheckboxSelectMultiple
# Register your models here.

# making image field in the django admin required
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

        class Meta:
            model = Product
            fields = '__all__'
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('product_name', 'price', 'stock', 'get_category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }