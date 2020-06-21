from selenium import webdriver
from constants import url
from constants import skill
from narutogame import Browser
from narutogame import BrowserError
from narutogame import Ninja
from narutogame import NinjaError
from narutogame import get_time
from time import sleep
import logging
import requestbot as rb

def get_accounts():
    accounts = []
    try:
        file = open('key')
        lines = file.readlines()
        for line in lines:
            email, senha = line.split()
            accounts.append([email, senha])
    except:
        pass
    return accounts

def make_browser():
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.get(url.HOME)
    return Browser(driver)

def start_play(email, password, interval, id=0):
    session = rb.Session()
    img_name = 'captcha_' + str(id)+ '.png'
    session.download_captcha(img_name)
    rb.show_image(img_name)
    captcha = input('Insira o captcha de ' + img_name + ' e aperte enter: ')
    session.login(email, password, captcha)
    characters = session.get_characters()
    for c in characters:
        session.select_character(c)
        session.get_fidelity()
        session.make_contest()
        
    while True:
        for c in characters:
            session.select_character(c)
            session.finish_mission()
            session.start_dojo_battle()
            session.battle()
            session.train_jutsus()
            session.train()
            session.do_first_task()
            session.do_first_mission()
        sleep(interval*60)
        

def play_story_mode(browser):
    ninjas = browser.get_ninjas()
    blows = [skill.KONOHA_TSU, skill.HENGE, skill.DYNAMIC_KICK, skill.PUNCH, skill.KICK]
    for ninja in ninjas:
        try:
            ninja.select()
            ninja.get_story_mod()
            ninja.figth(blows)
        except:
            logging.exception('play_story_mode error')
        
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

