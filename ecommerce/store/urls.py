from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name='store'),
    path('<slug:category_slug>/', views.store, name='products_by_category'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('cookie/', views.manageCookie, name='cookie'),
]
