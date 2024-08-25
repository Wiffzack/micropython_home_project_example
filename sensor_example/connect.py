from machine import ADC, Pin
from time import sleep
import socket
import utime as time
import socket # For Building TCP Connection
import network
import urequests
import time
from machine import WDT
wdt = WDT()  # enable it with a timeout of 2s


# WLAN-Konfiguration
wlanSSID = 'Magenta49748'
wlanPW = 'master314.'

def wait_for_internet_connection():
    while True:
        try:
            response = urequests.get("http://192.168.137.39:8080")
            print ("connected")
            break
        except:
            print ("wait for device")
            time.sleep(2)
            pass

def wlanConnect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen')
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print('.')
            wdt.feed()
            time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt')
        netConfig = wlan.ifconfig()
        print('IPv4-Adresse:', netConfig[0])
        print()
        #wait_for_internet_connection()
        return netConfig[0]
    else:
        print('Keine WLAN-Verbindung')
        print('WLAN-Status:', wlan.status())
        print()
        return ''