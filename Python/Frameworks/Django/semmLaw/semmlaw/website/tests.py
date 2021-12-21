from django.test import TestCase

from .models import Newsfeed


class NewsfeedModelTests(TestCase):

    def google_news_api_feeds_news(self):
        """
        news returns True when fed by Google News API
        """
        self.assertIs(Newsfeed.news(), True)
