## Copyright (c) 2019 aNoken

import network
from machine import SPI
from Maix import GPIO
from fpioa_manager import fm, board_info
import utime
from machine import UART

fm.register(6, fm.fpioa.UART2_TX, force=True)
fm.register(7, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

while(True):
    if uart_Port.any()!=0:
        a=uart_Port.readline()
        print("in",a)


