from selenium import webdriver
from narutogame import Browser
from time import sleep
from auto_play import *
import sys

accounts = get_accounts()
for key in accounts:
    request_bot(*key, do_first_task=False, get_fidelity=False)
    b = make_browser()
    b.login(*key)
    #input('Escreva o captcha, logue e aperte enter...')
    #play_story_mode(b)
    
