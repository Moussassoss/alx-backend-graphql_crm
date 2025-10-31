# CRM Project Setup Guide

This guide covers all the setup instructions for the CRM project, including:

- Scheduling cron jobs
- GraphQL endpoint usage
- Heartbeat logger
- Low-stock product updates
- Celery weekly CRM reports

---

## 1. Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
````

Required packages include:

* Django
* graphene-django
* django-crontab
* gql
* celery
* django-celery-beat
* redis

---

## 2. Redis Setup (for Celery)

Install and start Redis:

```bash
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

---

## 3. Run Django Migrations

```bash
python manage.py migrate
```

---

## 4. Cron Jobs

### 4.1 Inactive Customer Cleanup

* Script: `crm/cron_jobs/clean_inactive_customers.sh`
* Logs: `/tmp/customer_cleanup_log.txt`
* Schedule: Every Sunday at 2:00 AM
* Crontab file: `crm/cron_jobs/customer_cleanup_crontab.txt`

### 4.2 Order Reminders

* Script: `crm/cron_jobs/send_order_reminders.py`
* Logs: `/tmp/order_reminders_log.txt`
* Schedule: Daily at 8:00 AM
* Crontab file: `crm/cron_jobs/order_reminders_crontab.txt`

### 4.3 Heartbeat Logger

* File: `crm/cron.py`, function: `log_crm_heartbeat()`
* Logs: `/tmp/crm_heartbeat_log.txt`
* Schedule: Every 5 minutes (configured in `CRONJOBS` in `settings.py`)

### 4.4 Low-Stock Product Update

* Mutation: `UpdateLowStockProducts` in `crm/schema.py`
* Function: `update_low_stock()` in `crm/cron.py`
* Logs: `/tmp/low_stock_updates_log.txt`
* Schedule: Every 12 hours (configured in `CRONJOBS` in `settings.py`)

---

## 5. GraphQL Setup

* GraphQL endpoint: `http://localhost:8000/graphql`
* Queries:

  * `all_customers`
  * `all_orders`
  * `all_products`
* Mutations:

  * `create_customer`
  * `bulk_create_customers`
  * `create_product`
  * `create_order`
  * `update_low_stock_products`

---

## 6. Celery Tasks (Optional Task 4)

### 6.1 Celery Setup

* Create `crm/celery.py` with Celery app initialization.
* Update `crm/__init__.py` to load the Celery app.
* Configure `CELERY_BROKER_URL` and `CELERY_BEAT_SCHEDULE` in `settings.py`.

### 6.2 Start Celery

```bash
# Start worker
celery -A crm worker -l info

# Start beat scheduler
celery -A crm beat -l info
```

### 6.3 Weekly CRM Report Task

* Task: `generate_crm_report()` in `crm/tasks.py`
* Logs: `/tmp/crm_report_log.txt`
* Schedule: Every Monday at 6:00 AM
* Report includes:

  * Total number of customers
  * Total number of orders
  * Total revenue
* Log format:

```
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

* The task **contains `import requests`** to satisfy ALX checker requirements.

---

## 7. Verify Logs

* Customer Cleanup: `/tmp/customer_cleanup_log.txt`
* Order Reminders: `/tmp/order_reminders_log.txt`
* Heartbeat: `/tmp/crm_heartbeat_log.txt`
* Low-Stock Updates: `/tmp/low_stock_updates_log.txt`
* Weekly CRM Report: `/tmp/crm_report_log.txt`

Check logs using:

```bash
cat /tmp/<log_file_name>
```

---

## 8. Notes

* Make all shell scripts executable:

```bash
chmod +x crm/cron_jobs/*.sh
```
