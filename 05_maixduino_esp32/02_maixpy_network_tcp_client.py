## Copyright (c) 2019 aNoken

import network, usocket
from Maix import GPIO
from fpioa_manager import fm, board_info
import time, image, lcd

WIFI_SSID = "your_ssid"
WIFI_PASSWD = "your_passwd"

server_ip      = "192.168.10.2"
server_port    = 8080

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,
    rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,
    miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

print("ESP32_SPI firmware version:", nic.version())

nic.connect(WIFI_SSID, WIFI_PASSWD)
print(nic.ifconfig())
print(nic.isconnected())

addr = (server_ip, server_port)

sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
sock.settimeout(1)

while True:
    sock.connect(addr)
    sock.settimeout(1)
    time.sleep(1)
    sock.send("hello\n".encode())
    data = sock.recv(256)
    print("Received:", data)
    sock.close()