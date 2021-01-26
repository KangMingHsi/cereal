import json
from django.http import HttpResponse, HttpResponseNotFound
from .models import Product
from .utils import convert_body


def check_product_id_and_stock(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        data = {}
        try:
            data = convert_body(request.body)
            if any(map(lambda x: not x, [data['product_id'], data['qty'], data['customer_id']])):
                return HttpResponseNotFound("there is empty input")
            product = Product.objects.get(product_id=data['product_id'])
            if product.stock_pcs < int(data['qty']):
                return HttpResponseNotFound("no enough product")
            if product.vip and not data['vip']:
                return HttpResponseNotFound("this product requires vip")
        except Product.DoesNotExist:
            return HttpResponseNotFound("product not found")

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def notify_if_stock(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        data = {}
        try:
            data = convert_body(request.body)
            pre_stock = Product.objects.get(product_id=data['product_id']).stock_pcs
            response = view_func(request, *args, **kwargs)
            if pre_stock == 0:
                return HttpResponse(f"There is stock for #{data['product_id']}")
        except Product.DoesNotExist:
            return HttpResponseNotFound("product not found")
        return response
    return _wrapped_view_func
