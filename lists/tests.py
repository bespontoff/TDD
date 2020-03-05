from lists.models import Item
from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'New item list'})
        self.assertIn('New item list', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTest(TestCase):

    def test_save_and_retrieve_items(self):
        first = Item()
        first.text = 'first item'
        first.save()

        second = Item()
        second.text = 'second item'
        second.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)
        self.assertEqual(saved_item[0].text, 'first item')
        self.assertEqual(saved_item[1].text, 'second item')
