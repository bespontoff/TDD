import time
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class UserViewTests(LiveServerTestCase):
    MAX_WAIT = 3

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_item_in_list(self, item):
        start_time = time.time()

        while True:
            try:
                todo_list = self.browser.find_element_by_id('todo_list')
                todo_items = todo_list.find_elements_by_tag_name('li')
                self.assertIn(item, [item.text for item in todo_items],
                              f'Not found added text in TODO list: {todo_list.text}')
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(.5)

    def test_view_home_page_with_todo_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
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

        self.wait_item_in_list('Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        inputbox = self.browser.find_element_by_id('add_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        # self.wait_item_in_list('Купить павлиньи перья')
        self.wait_item_in_list('Сделать мушку из павлиньих перьев')

    def test_users_can_start_different_lists(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('add_item')
        inputbox.send_keys('Buy soup')
        inputbox.send_keys(Keys.ENTER)
        self.wait_item_in_list('Buy soup')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy soup', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        inputbox = self.browser.find_element_by_id('add_item')
        inputbox.send_keys('go to movie')
        inputbox.send_keys(Keys.ENTER)
        self.wait_item_in_list('go to movie')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(edith_list_url, francis_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy soup', page_text)
        self.assertIn('go to movie', page_text)

        # Она посещает этот URL-адрес – ее список по-прежнему там.
        # Удовлетворенная, она снова ложится спать
        # self.fail('Дописать тест')
