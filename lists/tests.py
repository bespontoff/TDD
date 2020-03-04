from django.http import HttpRequest
from django.test import TestCase

# Create your tests here.
from django.urls import resolve
from.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
