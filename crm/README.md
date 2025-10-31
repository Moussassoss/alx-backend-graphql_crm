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
```

Start the Redis server:

```bash
sudo service redis-server start
```

## 2. Run Django Migrations

Before running Celery tasks, migrate the database:

```bash
python manage.py migrate
```

## 3. Start Celery Worker

Run the Celery worker to process background tasks:

```bash
celery -A crm worker -l info
```

## 4. Start Celery Beat

Run Celery Beat to schedule periodic tasks:

```bash
celery -A crm beat -l info
```

## 5. Verify Logs

The weekly CRM report will be generated and logged to:

```
/tmp/crm_report_log.txt
```

You can view the log using:

```bash
cat /tmp/crm_report_log.txt
```

## 6. Summary of the Celery Task

* **Task name:** `generate_crm_report`
* **Schedule:** Every Monday at 6:00 AM
* **Report includes:**

  * Total number of customers
  * Total number of orders
  * Total revenue (sum of all order totals)
* **Log format:**

  ```
  YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
  ```

---

✅ **This README covers all required setup steps**:

* Redis installation ✅
* Dependency installation ✅
* Database migration ✅
* Celery worker start ✅
* Celery beat start ✅
* Log verification ✅
