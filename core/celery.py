import os
from celery import Celery

# SET THE DEFAULT DJANGO SETTINGS MODULE FOR THE 'CELERY' PROGRAM.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# CREATE A CELERY INSTANCE AND CONFIGURE IT USING THE SETTINGS FROM DJANGO.
app = Celery('gov_portal_backend')

# LOAD TASK MODULES FROM ALL REGISTERED DJANGO APP CONFIGS.
# CELERY WILL LOOK FOR A 'TASKS.PY' FILE IN EACH APP.
app.config_from_object('django.conf:settings', namespace='CELERY')

# AUTO-DISCOVER TASKS IN ALL INSTALLED APPS.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
