from network import WLAN, STA_IF
from time import sleep


wlan = WLAN(STA_IF)
wlan.active(True)

wlan.connect('RT', 'ronytoss', 5000)
# wlan.connect('oopho6bo', 'pestilence', 5000)

while not wlan.isconnected():
    sleep(1)
