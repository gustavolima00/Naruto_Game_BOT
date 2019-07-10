from selenium import webdriver
from constants import *
class BrowserError(Exception):
    pass

class Browser:
    def __init__(self, driver):
        self.driver = driver
    def login(self, email, password):
        self.get_page(HOME_URL)
        header = self.driver.find_element_by_id(FORMULARIO_ID)
        email_box = header.find_element_by_id(EMAIL_ID)
        password_box = header.find_element_by_id(PASSWORD_ID)
        email_box.send_keys(email)
        password_box.send_keys(password)
    def get_current_page(self):
        return self.driver.current_url
    def get_page(self, url):
        current_url = self.get_current_page()
        if current_url == url:
            return True
        self.driver.get(url)
        current_url = self.get_current_page()
        if current_url == url:
            return True
        raise BrowserError('Erro ao acessar {}'.format(url))