from celery import Celery


class Celerizer:
    def __init__(self, include, backend='redis://app_redis:6379', broker='redis://app_redis:6379'):
        self._celery_app = None
        self.backend = backend
        self.broker = broker
        self.include = include

    @property
    def celery_app(self):
        if self._celery_app is None:
            self._celery_app = Celery(
                backend=self.backend,
                broker=self.broker,
                include=self.include)
        return self._celery_app


celerizer = Celerizer(['bot'])
celery = celerizer.celery_app
