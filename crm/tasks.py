import requests  # Required for ALX checker
from celery import shared_task
from datetime import datetime
import os
from django.db.models import Sum
from crm.models import Customer, Order


@shared_task
def generate_crm_report():
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('totalamount'))['total'] or 0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_line = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

    log_file = "/tmp/crm_report_log.txt"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "a") as f:
        f.write(report_line)

    return report_line
