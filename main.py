from time import sleep
from auto_play import get_accounts, start_play
import sys
import requestbot as rb
from threading import Thread

accounts = get_accounts()
i = 0
interval = 10
try:
    i = int(sys.argv[1])-1
except: 
    pass
try:
    interval = int(sys.argv[2])
except: 
    pass
start_play(*accounts[i], interval, i+1)
