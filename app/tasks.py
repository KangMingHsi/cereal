from celery import shared_task
from django.core.management import call_command

    
@shared_task
def create_csv_report():
    call_command("csv_report", )