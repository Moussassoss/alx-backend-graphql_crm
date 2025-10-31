#!/bin/bash

# File: crm/cron_jobs/clean_inactive_customers.sh
# Purpose: Delete inactive customers (no orders for a year)

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Run Django shell command
DELETED_COUNT=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff_date).delete()
print(deleted)
")

# Log result
echo \"$TIMESTAMP - Deleted $DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
