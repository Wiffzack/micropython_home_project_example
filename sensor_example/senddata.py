# Bibliotheken laden
from machine import Pin, I2C
from machine import SoftI2C
import connect
import bme280
import ath10
import json
import urequests
import socket
import time
import machine
import time
from machine import WDT
wdt = WDT()  

i2c_sda = Pin(4)
i2c_scl = Pin(5)

# Initialisierung I2C
#i2c = I2C(sda=i2c_sda,scl=i2c_scl,freq=100000)
i2c = SoftI2C(sda=i2c_sda,scl=i2c_scl,freq=100000)

connect.wlanConnect()


# I2C-Bus-Scan
# Nicht überspringen da hier sehr wahrscheinlich der Fehler liegt.
print('Scan I2C Bus...')
devices = i2c.scan()

# Scanergebnis ausgeben für debug reasons...
if len(devices) == 0:
    print('Kein I2C-Gert gefunden!')
else:
    print('I2C-Gerte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))

bme = bme280.BME280(i2c=i2c)

print(bme.values)      

sensor = ath10.AHT10(i2c)
pumpe_out = machine.Pin(14, machine.Pin.OUT)

print("\nTemperature: %0.2f C" % sensor.temperature)
print("Humidity: %0.2f %%" % sensor.relative_humidity)

###curl -v -X POST http://192.168.137.1:8080/api/v1/NMcv2wbribw67YIy7Oib/telemetry --header Content-Type:application/json --data "{temperature:25}"
#data = {"temperature": sensor.temperature}
#response = urequests.post("http://192.168.137.1:8080/api/v1/NMcv2wbribw67YIy7Oib/telemetry", data=json.dumps(data))

def wait_for_internet_connection():
    while True:
        try:
            # ping url to check for connection!
            response = urequests.get("http://192.168.137.39:8080")
            print ("connected")
            break
        except:
            print ("wait for device")
            time.sleep(30)
            pass
        
# Bsp für einen Webserver
def web_page():
    gpio_state ="true"
    html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
    return html        

def send_data():
    headers = {
        "Content-Type": "application/json"
    }
    url = f"http://192.168.137.39:8080/api/v1/NMcv2wbribw67YIy7Oib/telemetry"
    start = time.ticks_ms()
    while True:
        wdt.feed()
        
        # conn, addr = s.accept()
        # print('Got a connection from %s' % str(addr))
        # request = conn.recv(1024)
        # request = str(request)
        # print('Content = %s' % request)
        # led_on = request.find('/?led=on')
        # led_off = request.find('/?led=off')
        # response = web_page()
        # conn.send('HTTP/1.1 200 OK\n')
        # conn.send('Content-Type: text/html\n')
        # conn.send('Connection: close\n\n')
        # conn.sendall(response)
        # conn.close()        
        
        try:
            adc = machine.ADC(0)
            earth_humidity = adc.read()
            payload = {
                "temperature" : sensor.temperature,
                "humidity" :  sensor.relative_humidity,
                "pressure" : (bme.get_pressure/100),
                "earth_humidity" : earth_humidity,
            }
            try:
                response = urequests.post(url, headers=headers, data=json.dumps(payload))
            except Exception as e:
                print (e)
                machine.reset()
                machine.lightsleep(1000)
            machine.lightsleep(1000)
        except Exception as e:
            print (e)
            machine.reset()
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
        
        
send_data()        
