# CRM Celery Integration

This module adds a scheduled Celery task that generates a weekly CRM report summarizing total customers, orders, and revenue.  
The report is automatically logged to `/tmp/crm_report_log.txt` every Monday at 6:00 AM.

---

## 🧰 Setup Instructions

### 1. Install Redis and Dependencies

Install Redis:
```bash
sudo apt install redis-server
