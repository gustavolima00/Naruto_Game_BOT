from selenium import webdriver
from constants import *
from narutogame import Browser

accounts = []
try:
    file = open('acc.txt')
    lines = file.readlines()
    for line in lines:
        email, senha = line.split()
        accounts.append([email, senha])
except:
    pass


driver = webdriver.Chrome('./chromedriver')
driver.get(HOME_URL)

b1 = Browser(driver)
b1.login(accounts[0][0], accounts[0][1])
