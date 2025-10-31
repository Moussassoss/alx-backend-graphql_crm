#!/bin/bash
# Deletes inactive customers (no orders for over a year)
# Logs the count to /tmp/customer_cleanup_log.txt

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Run Django shell command and capture count
count=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=365)
count, _ = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff_date).delete()
print(count)
")

# Log the result
echo \"$TIMESTAMP - Deleted $count inactive customers\" >> /tmp/customer_cleanup_log.txt
