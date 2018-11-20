#!/usr/bin/env python
import elevate
import time
import serial
import platform
import sys
import os
import serial.tools.list_ports as port_list

def eval_priv():
    if platform.system() == 'Linux':
        elevate.elevate(graphical=False)
        print(f"UID: {os.getuid()}")
    else:
        elevate.elevate(show_console=True)


def initialize(ser):
    inicijalitiraj = input("Do you want to inizialize the module? (0-No / 1-yes): ")
    if inicijalitiraj == '1':
        print("starting initialization...")
        #Lista AT naredbi koja će se poslati preko USB porta na komunikacijski modul kako bi ga inicijalizirala
        init_commands = ["AT\r\n", "AT+CPIN?\r\n", "AT+CREG?\r\n", "AT+CREG=1\r\n", "AT+CREG?\r\n", \
        'AT+CGDCONT=1,"IP","internet.tele2.hr"\r\n', "AT+CGACT=1\r\n", "AT+CGPADDR=1\r\n"]

        for init_command in init_commands:
            print(f"about to exec: {init_command}")
            ser.write(init_command.encode())
            if init_command == 'AT+CGACT=1\r\n':
                print("going to sleep a bit longer...")
                time.sleep(10)
            else:
                time.sleep(5)
            response = ser.read_all()
            response = response.decode('utf-8')
            print(response)
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        UDP_commands = ['AT+upsd=0,1,"hologram"\r\n', 'AT+upsda=0,3\r\n', 'AT+usocr=17,1000\r\n']
        print("Creating UDP socket on client...")
        for UDP_command in UDP_commands:
            print(f"about to exec: {UDP_command}")
            ser.write(UDP_command.encode())
            time.sleep(5)
            resp = ser.read_all()
            resp = resp.decode('UTF-8')
            print(resp)
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    else:
        pass

def send_UDP_data(ser):
    UDP_data = input("Enter data you want to send to the server: ")
    send_over_UDP_command = f'AT+USOST=0,"{serverIP}",{serverUDP},{len(UDP_data)},"{UDP_data}"\r\n'
    ser.write(send_over_UDP_command.encode())
    time.sleep(0.5)
    print(ser.read_all().decode())


if __name__ == '__main__':
    eval_priv()

    #Pregled dostupnih portova
    ports = list(port_list.comports())
    for p in ports:
        print(p)

    PORT = input("Unesite naziv porta: ")
    ser = serial.Serial(PORT, 115200, timeout=10)
    print(f"Device: {ser.name}")
    ser.close() #Iz nekog razloga govori da je port otvoren kada nije (isprobao sam izvaditi kabel i ponovo ga vratiti i pokrenuti app i opet vraca istu gresku)
    ser.open()
    print(f"Opened: {ser.is_open}")

    initialize(ser)

    serverIP = '142.93.104.222'
    serverUDP = 9000

    hardcoded = input("Do you want to use hardcoded server socket info or specify yours? (Type '0' to use hardcoded or '1' to specify your own server): ")
    if hardcoded == '1':
        serverIP = input("Enter server IP: ")
        serverUDP = input("Enter server UDP port no.: ")
    else:
            pass

    print(f"{serverIP}, {serverUDP}")

    while True:
        send_UDP_data(ser)
        answ = input("do you want to send more data? (0-No / 1-Yes)")
        if answ == '0':
            break
        else:
            pass
    time.sleep(1)
    print("zatvaram program...")
    #Zatvaranje USB porta prije završetka programa
    ser.close()