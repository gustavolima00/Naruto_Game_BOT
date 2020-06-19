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

def make_session():
    return rb.start_session()

def request_bot(email, password, train=True, train_first_jutsu=True, do_first_task=True, do_first_mission=True):
    session = rb.start_session()
    rb.dowload_captcha(session)
    rb.show_image('captcha.png')
    captcha = input('Insira o captcha e aperte enter...')
    rb.login(session, email, password, captcha)
    characters = rb.get_characters(session)
    for c in characters:
        rb.select_character(session, c)
        rb.finish_mission(session)
        if train:
            rb.train(session)
        if train_first_jutsu:
            rb.train_first_jutsu(session)
        if do_first_task:
            rb.do_first_task(session)
        if do_first_mission:
            rb.do_first_mission(session)

def play_story_mode(browser):
    ninjas = browser.get_ninjas()
    blows = [skill.PUNCH, skill.KICK, skill.HAND_DEFEND, skill.ACROBACY]
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

