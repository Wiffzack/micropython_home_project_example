# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine
import gc
import network
from machine import WDT
gc.collect()
wdt = WDT()  # enable it with a timeout of 2s
wdt.feed()


# I recommend to disable WLAN until its needed!
# Not for energy saving , but for the fact thats its become hot
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# start main loop
import senddata


