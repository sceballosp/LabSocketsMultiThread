import socket 
import threading
import Constantes
import os
from setuptools import Command
import shutil

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def tipo_archivo(file):

    if(file.endswith('.jpg')):
        mimetype = 'image/jpg'
    elif(file.endswith('.css')):
        mimetype = 'text/css'
    elif(file.endswith('.pdf')):
        mimetype = 'application/pdf'
    else:
        mimetype = 'text/html'

    return mimetype


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        comm = msg_length.split()
        command = comm[0]
        print(f'Received from { addr }')
        print(command)
        
        if command == Constantes.GET:
            file = open(Constantes.PATH + f'/{ comm[1] }') 
            files = file.read()
            try:
                conn.sendall(bytes(files, FORMAT))
               
            except OSError:
                conn.send(bytes(f'[305] FILE NOT FOUND', FORMAT))
            else:
                conn.send(bytes(f'[305] ok', FORMAT))

                

        elif command == Constantes.QUIT:
            print(f'[CLIENT DISCONNECTED] { addr } disconnected')
            conn.send(bytes(f'[600] DISCONNECTED', FORMAT))
            connected = False


        elif command == Constantes.DELETE:
            file = Constantes.PATH + f'/{ comm[1] }'
            try:
                os.remove(file)
            except OSError:
                conn.send(bytes(f'[305] FILE NOT FOUND', FORMAT))
            else:
                conn.send(bytes(f'[201] FILE DELETED', FORMAT))

        elif command == Constantes.PUT:
            file = comm[1]
            try:
                shutil.copy(file, Constantes.PATH)
            except:
                conn.send("[401] FAILED TO UPLOAD".encode(FORMAT))
            else:
                conn.send("[400] FILE UPLOADED".encode(FORMAT))

        elif command == Constantes.HEAD:
            pass

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