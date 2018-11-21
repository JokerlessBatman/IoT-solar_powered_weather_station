#!/usr/bin/python3
import socket

IP = '142.93.104.222'
PORT = 9000

print(f"IP address: {IP}")
print(f"PORT:       {PORT}")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print("initialized!")

while True:
    print("waiting to receive data from clients!")
    data, address = sock.recvfrom(4096)
    data = data.decode('utf-8')
    client_IP = address[0]
    client_PORT = address[1]
    sock_to_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_to_client.sendto("ACK".encode(), (client_IP, client_PORT))
    print(f"From {client_IP}:{client_PORT} {data}")
    print(type(data))
    print()
