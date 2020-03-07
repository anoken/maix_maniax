## Copyright (c) 2019 aNoken

import network,lcd
from Maix import GPIO
from fpioa_manager import fm, board_info

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10)#SPI cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#SPI mosi
fm.register(26,fm.fpioa.GPIOHS14)#SPI miso
fm.register(27,fm.fpioa.GPIOHS15)#SPI sclk

lcd.init()
lcd.clear()

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,
	rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,
	miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

print("ESP32_SPI firmware version:", nic.version())

enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK"]
aps = nic.scan()
cnt=0
for ap in aps:
    enc_1="SSID:{:^20}".format(ap[0])
    enc_2="    ENC:{:>5} , RSSI:{:^20}".format(enc_str[ap[1]], ap[2])
    lcd.draw_string(0, 0+20*(2*cnt), enc_1, lcd.WHITE, lcd.RED)
    lcd.draw_string(0, 0+20*(2*cnt+1), enc_2, lcd.WHITE, lcd.RED)
    print(enc_1)
    print(enc_2)
    cnt=cnt+1
    
    