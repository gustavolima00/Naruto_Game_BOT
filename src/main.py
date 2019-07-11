from selenium import webdriver
from constants import *
from narutogame import Browser
from time import sleep
from auto_play import *

accounts = get_accounts()
b1 = make_browser()

b1.login(*accounts[0])
input('Escreva o captcha, logue e aperte enter...')

make_tasks(b1, 50)
ninja = b1.get_ninjas()[1]
blows = [PUNCH, KICK, HAND_DEFEND, ACROBACY]

ninja.figth(blows)