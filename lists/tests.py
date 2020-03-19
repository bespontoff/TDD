from lists.models import Item, List
from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelTest(TestCase):

    def test_save_and_retrieve_items(self):
        list_ = List()
        list_.save()

        first = Item()
        first.text = 'first item'
        first.list = list_
        first.save()

        second = Item()
        second.text = 'second item'
        second.list = list_
        second.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)
        self.assertEqual(saved_item[0].text, 'first item')
        self.assertEqual(saved_item[1].text, 'second item')
        self.assertEqual(saved_item[0].list, list_)
        self.assertEqual(saved_item[1].list, list_)

    def test_save_item_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)

        response = self.client.get('/lists/cool-list')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/cool-list')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_redirect_after_post_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'New item list'})
        self.assertRedirects(response, '/lists/cool-list')

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'New item list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item list')
