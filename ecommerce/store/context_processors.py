
from .models import Category

def menu_links(request):
    categories = Category.objects.order_by('name')
    print(type(categories))
    return {'categories':categories}
