from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    stock_pcs = models.IntegerField()
    price = models.IntegerField()
    shop_id = models.CharField(max_length=16)
    vip = models.BooleanField()

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    shop_id = models.CharField(max_length=16)
    customer_id = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
