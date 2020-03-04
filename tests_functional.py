import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class UserViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_view_home_page_with_todo_list_and_retrieve_it_later(self):
        self.browser.get('http://127.0.0.1:8000')
        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('TODO', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('add_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a TODO item')
        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        todo_list = self.browser.find_element_by_id('todo_list')
        todo_items = todo_list.find_elements_by_tag_name('li')
        self.assertTrue(any(item.text == 'Купить павлиньи перья' for item in todo_items),
                        'Not found added text in TODO list')
        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        self.fail('Дописать тест')
        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        # Она посещает этот URL-адрес – ее список по-прежнему там.
        # Удовлетворенная, она снова ложится спать


if __name__ == '__main__':
    unittest.main()
