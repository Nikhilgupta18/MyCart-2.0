from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import *


# Create your views here.


def index(request):
    data = userCart(request)

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': data['cartItems']
    }
    return render(request, 'index.html', context)


def cart(request):
    data = userCart(request)
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems']
    }
    return render(request, 'cart.html', context)


def checkout(request):
    data = userCart(request)
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems']
    }
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def placeOrder(request):
    # print('Data: ', request.body)
    transactionID = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestCheckout(request, data)

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        state=data['shipping']['state'],
        city=data['shipping']['city'],
        zip_code=data['shipping']['zipcode'],
    )
    total = float(data['form']['total'])
    order.transaction_id = transactionID
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('payment submitted', safe=False)
