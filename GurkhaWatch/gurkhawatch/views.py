from django.shortcuts import render

def home(request):
    return render(request, 'index.html', {'variable1':'This is for tailwind css'})