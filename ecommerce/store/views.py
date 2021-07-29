from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def store(request):
    title = "Store"
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html',context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html',context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html',context)
