from django.contrib import admin
from .models import Category
from django import forms
from django.db.models import fields
# Register your models here.

# making image field in the django admin required
class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_image'].required = True

        class Meta:
            model = Category
            fields = '__all__'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    #pre populate slug field based on category name
    list_display = ('category_name', 'slug',)
    prepopulated_fields = {'slug':('category_name',)}