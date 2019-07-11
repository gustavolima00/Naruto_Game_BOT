from selenium import webdriver
from constants import HOME_URL
from narutogame import Browser
from narutogame import BrowserError
from narutogame import Ninja
from narutogame import NinjaError
from narutogame import get_time
from time import sleep

def get_accounts():
    accounts = []
    try:
        file = open('acc.txt')
        lines = file.readlines()
        for line in lines:
            email, senha = line.split()
            accounts.append([email, senha])
    except:
        pass
    return accounts

def make_browser():
    driver = webdriver.Chrome('./chromedriver')
    driver.get(HOME_URL)
    return Browser(driver)

def make_tasks(browser, times=3):
    tmp = browser.get_ninjas()
    dct = {}
    for x in tmp:
        dct[x] = get_time()
    for _ in range(times):
        ninja, _ = sorted(dct.items(), key = lambda kv:(kv[1], kv[0]))[0]
        print('Ninja selecionado: {}'.format(ninja.name))
        dct[ninja] = get_time()
        try:
            ninja.select()
            ninja.get_mission()
        except NinjaError as err:
            print('NijaError: {}'.format(err))
        except BrowserError as err:
            print('BrowserError: {}'.format(err))

        try:
            time = ninja.make_task()
            dct[ninja] = time
        except NinjaError as err:
            print('NijaError: {}'.format(err))
        except BrowserError as err:
            print('BrowserError: {}'.format(err))
