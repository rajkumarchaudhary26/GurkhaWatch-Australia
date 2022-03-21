from django.db.models.fields import EmailField
from django.shortcuts import render
from shop.models import Product
from category.models import Category
from productslider.models import ProductSlider
from django.core.mail import send_mail
from django.contrib import messages

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
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            'Message from ' + first_name + last_name,  # subject
            message,  # message
            email,  # from email
            ['info@gurkhawatch.com'],  # to email
        )

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        messages.success(
            request, 'Dear ' + first_name + last_name + ', we have received your message. We will repond shortly.')
        return render(request, 'contact.html', context)
    else:
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
