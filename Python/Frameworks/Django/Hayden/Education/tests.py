import datetime

from django.test import TestCase, modify_settings
from django.utils import timezone


@modify_settings(MIDDLEWARE={
    'append': 'django.middleware.cache.FetchFromCacheMiddleware',
    'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
})
class MiddlewareTestCase(TestCase):
    time = timezone.now() + datetime.timedelta(days=30)

    def test_cache_middleware(self):
        response = self.client.get('/')
