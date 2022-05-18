from ast import Break
from email import header
import socket
import os
import Constantes


HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def start():
    print('Client is running...')
    print('Enter \"quit\" to exit')
    print('ComMands: GET, HEAD, DELETE, POST, QUIT')
    print('Input commands:')
    
    command = input()
    while command != Constantes.QUIT:
        comm = command.split()
        if command == "":
            print('Please put a valid comand')
            command= input

        elif command == Constantes.GET:
            client.send(bytes(command, FORMAT))     
            print(client.recv(HEADER).decode(FORMAT))

        elif command == Constantes.DELETE:
            client.send(bytes(command, FORMAT))
            data_received = client.recv(HEADER,FORMAT)        
            print(data_received.decode(FORMAT))
        
        else:
            client.send(bytes( command, FORMAT))
            print(client.recv(HEADER).decode(FORMAT))

    client.send(bytes(command, FORMAT))
    data_received = client.recv(HEADER,FORMAT)        
    print(data_received.decode(FORMAT))
    print('Closing connection...BYE BYE...')
       

start()



