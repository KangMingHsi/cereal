import datetime
import csv
from django.core.management.base import BaseCommand, CommandError

from app.models import Order

class Command(BaseCommand):
    help = 'Generates order records'

    def handle(self, *args, **options):
        orders = Order.objects.filter(
            created_at__gte=datetime.date.today() - datetime.timedelta(days=1))

        records = {}
        for order in orders:
            shop_record = records.setdefault(order.shop_id, {'Shop': order.shop_id})
            shop_record['earns'] = shop_record.get('earns', 0) + order.price
            shop_record['amount'] = shop_record.get('amount', 0) + order.qty
            shop_record['orders'] = shop_record.get('orders', 0) + 1

        if records:
            with open(f'app/reports/reports_{datetime.date.today()}.csv', 'w+') as f:
                fieldnames = ['Shop', 'earns', 'amount', 'orders']
                writer = csv.DictWriter(f, fieldnames = fieldnames)
                writer.writeheader()
                writer.writerows(records.values())
            self.stdout.write('report success')
        else:
            self.stdout.write('no order today')