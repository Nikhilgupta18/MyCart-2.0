import json
from .models import *


def guestCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_cart_total': 0,
        'get_delivery_fee': 0,
        'get_cart_subtotal': 0,
        'get_cart_items': 0,

    }
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_subtotal'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass

    if 0 < order['get_cart_subtotal'] < 1000:
        order['get_delivery_fee'] = 100
        order['get_cart_subtotal'] += order['get_delivery_fee']
    order['get_cart_total'] = order['get_cart_subtotal']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def userCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartData = guestCart(request)
        items = cartData['items']
        order = cartData['order']
        cartItems = cartData['cartItems']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestCheckout(request, data):
    print('Anonymous User')
    name = data['form']['name']
    email = data['form']['email']

    guestCartData = guestCart(request)
    items = guestCartData['items']
    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
