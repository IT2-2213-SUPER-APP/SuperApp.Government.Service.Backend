# THIS WILL MAKE SURE THE APP IS ALWAYS IMPORTED WHEN
# DJANGO STARTS SO THAT SHARED_TASK WILL USE THIS APP.

from .celery import app as celery_app

__all__ = ('celery_app',)
