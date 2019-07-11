from selenium import webdriver
from narutogame import Browser
from time import sleep
from auto_play import *

accounts = get_accounts()
b1 = make_browser()
b1.login(*accounts[0])
input('Escreva o captcha, logue e aperte enter...')

play_story_mode(b1)