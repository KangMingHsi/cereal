from django.shortcuts import render
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .models import Product, Order
from .utils import convert_body
from .decorators import (check_product_id_and_stock,
                         notify_if_stock)


def index(request):
    context = {
        'products': Product.objects.all(),
        'orders': Order.objects.all(),
    }
    return render(request, 'index.html', context)

@require_http_methods(["POST"])
@check_product_id_and_stock
def add_order(request, *args, **kwargs):
    data = convert_body(request.body)
    qty = int(data['qty'])
    product = Product.objects.get(product_id=data['product_id'])
    product.stock_pcs -= qty
    with transaction.atomic():
        Order(
            product=product,
            qty=qty,
            price=(product.price * qty),
            shop_id=product.shop_id,
            customer_id=data['customer_id']).save()
        product.save()
    return HttpResponse("Add successfully")

@require_http_methods(["DELETE"])
@notify_if_stock
def delete_order(request, *args, **kwargs):
    data = convert_body(request.body)
    product = Product.objects.get(product_id=data['product_id'])
    order = Order.objects.get(id=data['order_id'])
    product.stock_pcs += data['qty']
    with transaction.atomic():
        order.delete()
        product.save()
    return HttpResponse("Delete successfully")

@require_http_methods(["GET"])
def top_three(request):
    orders = Order.objects.all()
    dic = {}
    for order in orders:
        product_id = str(order.product.product_id)
        dic[product_id] = dic.get(product_id, 0) + order.qty
    top_three = sorted(dic.keys(), key=lambda x: dic[x], reverse=True)[:3]
    message = ('Top three product ' + ', '.join(top_three) + ' in order.'
               if top_three else 'no any order to compute top three')
    return HttpResponse(message)
