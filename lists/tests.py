from django.http import HttpRequest
from django.test import TestCase

# Create your tests here.
from django.urls import resolve
from.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'New item list'})
        self.assertIn('New item list', response.content.decode())
