from django.shortcuts import render
from .models import Post
from django.views import generic
# Create your views here.


def post_list(request):
    post_list = Post.objects.all()
    print("hello")
    context = {
        'post_lists': post_list,
    }
    return render(request, 'blog.html', context)


class postDetail(generic.DetailView):
    model = Post
    template_name = 'single_blog.html'
