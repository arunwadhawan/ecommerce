from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *

# Create your views here.

def store(request):
    title = "Store"
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0, }
        cartItems = order['get_cart_items']

    products = Product.objects.all().filter(is_available=True)
    context = {'products':products,'order':order, 'items':items,'cartItems':cartItems,'shipping':False}

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
