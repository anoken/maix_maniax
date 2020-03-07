## Copyright (c) 2019 aNoken

from machine import SPI
from Maix import GPIO
from fpioa_manager import fm, board_info
import utime

fm.register(25,fm.fpioa.SPI1_SS0)#cs
fm.register(28,fm.fpioa.SPI1_D0)#mosi
fm.register(26,fm.fpioa.SPI1_D1)#miso
fm.register(27,fm.fpioa.SPI1_SCLK)#sclk

spi01=SPI(SPI.SPI1,mode=SPI.MODE_MASTER,baudrate=10000000,polarity=0,phase=0,bits=8,firstbit=SPI.MSB,mosi=fm.fpioa.SPI1_D0,miso=fm.fpioa.SPI1_D1,sck=fm.fpioa.SPI1_SCLK,cs0=fm.fpioa.SPI1_SS0)

buff=bytearray([0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08])
r_buff = bytearray(8)

spi01.write(buff, cs=SPI.CS0)
print(buff)
utime.sleep_ms(100)

spi01.write_readinto(buff, r_buff)
print(buff,r_buff)
utime.sleep_ms(100)
