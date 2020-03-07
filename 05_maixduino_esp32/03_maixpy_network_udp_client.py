## Copyright (c) 2019 aNoken

import network, usocket
from Maix import GPIO
from fpioa_manager import fm, board_info

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

sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
sock.settimeout(1)

cnt=0
while True:
    message="send_"+str(cnt)+"\n"
    sock.sendto(message.encode(),(server_ip, server_port))
    cnt=cnt+1
    time.sleep_ms(500)
sock.close()