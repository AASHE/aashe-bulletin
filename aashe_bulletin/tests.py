from django.http import HttpRequest
from django.test import TestCase

from .views import (AllItemsView,
                    FAQView,
                    LatestNewsFeedView,
                    NoSearchForYouView,
                    SubmissionGuidelinesView)


class ViewTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'GET'


class AllItemsViewTestCase(ViewTest):

    def test_get_succeeds(self):
        """Does GET succeed?"""
        response = AllItemsView.as_view()(self.request)
        self.assertEqual(200, response.status_code)


class FAQViewTestCase(ViewTest):

    def test_get_succeeds(self):
        """Does GET succeed?"""
        response = FAQView.as_view()(self.request)
        self.assertEqual(200, response.status_code)


class LatestNewsFeedViewTestCase(ViewTest):

    def test_get_succeeds(self):
        """Does GET succeed?"""
        response = LatestNewsFeedView()(self.request)
        self.assertEqual(200, response.status_code)


class NoSearchForYouViewTestCase(ViewTest):

    def test_get_succeeds(self):
        """Does GET succeed?"""
        response = NoSearchForYouView.as_view()(self.request)
        self.assertEqual(200, response.status_code)


class SubmissionGuidelinesViewTestCase(ViewTest):

    def test_get_succeeds(self):
        """Does GET succeed?"""
        response = SubmissionGuidelinesView.as_view()(self.request)
        self.assertEqual(200, response.status_code)
