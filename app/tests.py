from django.test import TestCase

from .models import Product, Order

# Create your tests here.
class OrderTestcase(TestCase):
    
    def setUp(self):
        self.p = Product.objects.create(
            product_id=10,
            stock_pcs=6,
            price=20,
            shop_id='tw',
            vip=True,
        )

        Order.objects.create(
            product=self.p,
            qty=1,
            price=self.p.price,
            shop_id=self.p.shop_id,
            customer_id=5,
        )

    def test_add_order(self):
        order = Order.objects.create(
            product=self.p,
            qty=1,
            price=self.p.price,
            shop_id=self.p.shop_id,
            customer_id=5,
        )
        self.assertEqual(order.id, 2)


    def test_delete_order(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.id, 1)
        order.delete()

    def test_top_three(self):
        """ Should test while server is up. """
        resp = self.client.get('http://localhost:8000/app/top_three/')
        self.assertEqual(resp.status_code, 200)
