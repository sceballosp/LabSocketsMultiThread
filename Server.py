import socket 
import threading
import Constantes
import os
from setuptools import Command

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        comm = msg_length.split()
        command = comm[0]
        print (f'Received from: {conn[0]}:{addr[1]}')
        print(command)
        
        if command == Constantes.GET:
            file =open(Constantes.PATH + f'/{ comm[1] }') 
            try:
                for line in file:
                    print(line) 
               
            except OSError
                conn.sendall(bytes(line),FORMAT) 
                
            else:
                 conn.send(bytes(f'[305] FILE NOT FOUND', FORMAT))

        elif command == Constantes.POST:
            pass


        
        elif command == Constantes.HEAD:
            pass




        elif command == Constantes.QUIT:
            connected = False
            pass


        elif command == Constantes.DELETE:
            file = Constantes.PATH + f'/{ comm[1] }'
            try:
                pass
                os.remove(file)
            except OSError:
                conn.send(bytes(f'[305] FILE NOT FOUND', FORMAT))
            else:
                conn.send(bytes(f'[201] FILE DELETED', FORMAT))


    conn.close()
        

def start():
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(ADDR)
    server.listen(10)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()