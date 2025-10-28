#!/bin/bash

# Log file location
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run Django shell command to delete inactive customers (no orders in the past year)
deleted_count=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(orders__isnull=True) | Customer.objects.exclude(orders__created_at__gte=one_year_ago)
deleted_count = deleted.count()
deleted.delete()
print(deleted_count)
")

# Log the timestamp and number of deleted customers
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $deleted_count\" >> $LOG_FILE
