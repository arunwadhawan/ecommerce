from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.db.models import Q
from django.contrib.auth import get_user_model
from analytics.signals import object_viewed_signal

User = get_user_model()

from .models import *

# Create your views here.

def store(request,category_slug=None):
    categories=None
    products = None
    title = "Store"
    if request.user.is_authenticated:
        print(request.user)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0, }
        cartItems = order['get_cart_items']

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        print(categories)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {'title':title,'products':products,'product_count':product_count,'order':order, 'items':items,'cartItems':cartItems,'shipping':False}

    return render(request, 'store/store.html',context)

def product_detail(request,category_slug, product_slug):
    title = "Product Details"
    try:       
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {'title':title,'product':product}
    object_viewed_signal.send(product.__class__,instance=product,request=request) # Send the Object viewed signal for analytics
    return render(request, 'store/product_detail.html',context)

def search(request):
    title = "Store"
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.all().filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
#    products = Product.objects.all().filter(is_available=True)
    context = {'title':title,'products':products}
    return render(request, 'store/store.html',context)

def cart(request):
    title = "Cart"
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
                items = []
                order = {'get_cart_total':0,'get_cart_items':0, }
                cartItems = order['get_cart_items']
    context = {'order':order, 'items':items,'cartItems':cartItems,'shipping':False}
    return render(request, 'store/cart.html',context)

def checkout(request):
    title = "Checkout"
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
                items = []
                order = {'get_cart_total':0,'get_cart_items':0, }
                cartItems = order['get_cart_items']
    context = {'order':order, 'items':items, 'cartItems': cartItems,'shipping':False}
    return render(request, 'store/checkout.html',context)

def updateItem(request):
    
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Action', action)
    print('Product ID', productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create( customer = customer , complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order,product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action =='remove':
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
        
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
    else:   
        print('User is not authenticated')

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            pincode = data['shipping']['pincode'],
            country = data['shipping']['country'],
            
            
            )
    
    return JsonResponse('Payment complete!', safe=False)

def manageCookie(request):
    print(request.COOKIES)
    print(request.session)
    print(dir(request.session))
    resp = HttpResponse('Wow')
    resp.set_cookie('zap',42)
    resp.set_cookie('wooprie', 42, max_age = 10)
    resp.set_cookie('radd', 42, max_age = 10)
    return resp
    return 
