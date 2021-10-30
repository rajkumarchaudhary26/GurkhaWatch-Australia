from django.shortcuts import render
from .models import ProductSlider

# Create your views here.


def product_slider(request):
    sliders = ProductSlider.objects.all()
    context = {
        'sliders': sliders,
    }
    return render(request, 'index.html', context)
