## Copyright (c) 2019 aNoken

import socket

HOST = '192.168.10.2'   
PORT = 8080
buffer_size = 256

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    msg, address = s.recvfrom(buffer_size)
    print("received",msg,address)

s.close()