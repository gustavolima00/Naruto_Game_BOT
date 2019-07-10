from selenium import webdriver
from constants import *

class BrowserError(Exception):
    pass

class Browser:
    def __init__(self, driver):
        self.driver = driver

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

    def login(self, email, password):
        self.get_page(HOME_URL)
        header = self.driver.find_element_by_id(FORMULARIO_ID)
        email_box = header.find_element_by_id(EMAIL_ID)
        password_box = header.find_element_by_id(PASSWORD_ID)
        email_box.send_keys(email)
        password_box.send_keys(password)

    def get_ninjas(self):
        self.get_page(NINJA_SELECT_URL)
        body = self.driver.find_element_by_id(RIGHT_ID)
        ninjas_imgs =  body.find_elements_by_css_selector(NINJA_SELECT_IMAGE_CSS)
        self.ninjas = []
        for button in ninjas_imgs:
            button.click()
            self.ninjas.append(Ninja(body))
    
    def select_ninja(self, ninja_name):
        self.get_page(NINJA_SELECT_URL)
        body = self.driver.find_element_by_id(RIGHT_ID)
        ninjas_imgs =  body.find_elements_by_css_selector(NINJA_SELECT_IMAGE_CSS)
        for button in ninjas_imgs:
            button.click()
            ninja = Ninja(body)
            if ninja.name == ninja_name:
                button = body.find_element_by_link_text('Jogar')
                button.click()
                return True
        raise BrowserError('Erro ao selecionar ninja: {}'.format(ninja_name))

class Ninja:
    def __init__(self, driver):
        self.name = driver.find_element_by_id(NINJA_NAME_ID).text
        self.level = driver.find_element_by_id(NINJA_LEVEL_ID).text
        self.ryous = driver.find_element_by_id(NINJA_RYOUS_ID).text