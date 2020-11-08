import os

from celery import Celery

# from django.conf import settings

# if settings.DEBUG:
#     settings =
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.production")

app = Celery("serious_shop")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
