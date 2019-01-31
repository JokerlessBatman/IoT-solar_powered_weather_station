#!/usr/bin/python3
import socket
import sys
import psycopg2
import time
import datetime
from ast import literal_eval


IP = '142.93.104.222'
PORT = 9000
MSG = b"Hello world!"
conn = None

sensors = {
    'wind': 45,
    'precipitation': 46,
    'humidity': 47,
    'temperature': 48
}

try:
    conn = psycopg2.connect("dbname = 'iotproject' user = 'iot_user' host = 'localhost' password = 'iot_password'")
except psycopg2.DatabaseError as ex:
    print("I am unable to connect the database: {0}".format(ex))
    sys.exit(1)

curs = conn.cursor()

def data_pushing(infos):
    date = datetime.datetime.now()
    for key, val in infos.items():
        curs.execute("INSERT INTO data (value, created_at, sensor_id) VALUES (%(info)s, %(date)s, %(id)s);", {'info': val, 'date': date, 'id': sensors[key]})
    conn.commit()


print(f"IP address: {IP}")
print(f"PORT:       {PORT}")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print("initialized!")

def data_transform(data):
    data['wind'] = round(data['wind'] * 0.667, 2)
    data['precipitation'] = data['precipitation'] * 10

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
    data_pushing(literal_eval(data))
    print()
