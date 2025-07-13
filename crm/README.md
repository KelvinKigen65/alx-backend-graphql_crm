# CRM Celery Setup Guide

## Prerequisites
- Redis server installed and running
- Python 3.8+ with virtual environment

## Installation
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start Redis (if not running):
```bash
redis-server
```

## Running Celery
1. Start Celery worker:
```bash
celery -A crm worker -l info
```

2. Start Celery Beat (for scheduled tasks):
```bash
celery -A crm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

3. (Optional) Start Flower for monitoring:
```bash
celery -A crm flower
```

## Verify Setup
Check the report logs:
```bash
tail -f /tmp/crm_report_log.txt
```

## Testing
Trigger a manual report generation:
```bash
python manage.py shell -c "from crm.tasks import generate_crm_report; generate_crm_report.delay()"
```