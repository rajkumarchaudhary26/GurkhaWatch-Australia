from django.shortcuts import render
from shop.models import Product
from category.models import Category
from productslider.models import ProductSlider

categories = [
    {
        'title': 'WATCHES',
        'count': 15
    },
    {
        'title': 'MENS WATCHES',
        'count': 6
    },
    {
        'title': 'ACCESSORIES',
        'count': 14
    },
    {
        'title': 'CASUAL WATCHES',
        'count': 9
    },
    {
        'title': 'SPORTS',
        'count': 1
    },
    {
        'title': 'URBAN CHRONO',
        'count': 3
    },
    {
        'title': 'G-200 EDITION',
        'count': 4
    },
    {
        'title': 'COMBAT',
        'count': 1
    },
    {
        'title': 'UPCOMING WATCHES',
        'count': 5
    },
]


'''
def home(request):
    return render(request, 'index.html', {
        'collections': list(range(1, 8)),
        'best_selling_products': list(range(1, 8))
    })
'''


def home(request):
    sliders = ProductSlider.objects.all()
    products = Product.objects.all().filter(is_available=True)
    collections = Category.objects.all()

    context = {'best_selling_products': products,
               'collections': collections, 'sliders': sliders}
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def upcoming_watches(request):
    return render(request, 'upcoming_watches.html')


def accessories(request):
    return render(request, 'accessories.html')


# def shop(request):
#     return render(request, 'shop.html', {
#         'categories': categories,
#         'products': list(range(1, 8))
#     })


# def category(request, slug):
#     return render(request, 'category.html', {
#         'title': slug,
#         'categories': categories,
#         'products': list(range(1, 8))
#     })
