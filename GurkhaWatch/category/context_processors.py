from .models import Category
# fetch all categories from the database


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
