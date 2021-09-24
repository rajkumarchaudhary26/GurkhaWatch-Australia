from django.contrib import admin
from .models import Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    #pre populate slug field based on category name
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug',)

admin.site.register(Category, CategoryAdmin)