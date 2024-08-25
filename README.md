# micropython_home_project_example
A simple micropython example page.

To write Micropython to  [ESP8266](https://www.micropython.org/download/ESP8266_GENERIC/) use [esptool.py](https://docs.espressif.com/projects/esptool/en/latest/esp32/).

Command to write:

> esptool.py --port COM0 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-FLASH_512K-20231227-v1.22.0.bin

Under Windows to find which COM Port the ESP8266 use, use the device manager. 
Under Ports something like USB-SERIAL CH340(COMX)
