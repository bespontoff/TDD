from selenium import webdriver
import unittest


class UserViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_view_home_page_with_todo_list(self):
        self.browser.get('http://127.0.0.1:8000')
        assert 'TODO' in self.browser.title


if __name__ == '__main__':
    unittest.main()