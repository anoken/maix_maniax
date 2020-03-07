## Copyright (c) 2019 aNoken
## 


import socket

server_ip = "192.168.XX.X"
server_port = 8080
listen_num = 5
buffer_size = 256

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((server_ip, server_port))
tcp_server.listen(listen_num)

while True:
    client,address = tcp_server.accept()
    print("connected",address)
    
    data = client.recv(buffer_size)
    print("received",data)
    
    client.send(b"ACK!!")
    client.close()