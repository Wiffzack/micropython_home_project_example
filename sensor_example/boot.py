# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine
import gc
import network
from machine import WDT
wdt = WDT()  # enable it with a timeout of 2s
wdt.feed()


gc.collect()



sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# start main loop
import senddata


