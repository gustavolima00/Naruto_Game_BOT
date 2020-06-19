from selenium import webdriver
from narutogame import Browser
from time import sleep
from auto_play import *

accounts = get_accounts()
b = make_browser()
b.login(*accounts[0])
input('Escreva o captcha, logue e aperte enter...')
play_story_mode(b)

request_bot(*accounts[0], do_first_task=False)
