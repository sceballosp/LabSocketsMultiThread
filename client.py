import socket
import constants
import os
import requests

save_path = 'C:/Users/Laura/Desktop/Universidad/Telematica/TestProyecto/clientFiles/'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1",constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"QUIT\" to exit')
    print('GET, POST, HEAD, DELETE,')
    print('Input commands:')
    command_to_send = input().split()

    while command_to_send != constants.QUIT:
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()                        
        elif (command_to_send[0] == constants.GET):

            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            filename = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT)
            completeName = os.path.join(save_path, filename)
            
            with open(completeName, "wb") as file:

                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
                print(data_received)
                file.write(data_received)

            #print(data_received.decode(constants.ENCONDING_FORMAT))
            print('Commands: GET, POST, HEAD, DELETE')
            print('Input commands:')
            command_to_send = input()  

        elif (command_to_send[0] == constants.POST):
            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            filename = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT)
            completeName = os.path.join(constants.FILE_DIRECTORY, filename)
            
            with open(completeName, "wb") as file:

                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
                print(data_received)
                file.write(data_received)

            #print(data_received.decode(constants.ENCONDING_FORMAT))
            print('Commands: GET, POST, HEAD, DELETE')
            print('Input commands:')
            command_to_send = input()  
    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()    

if __name__ == '__main__':
    main()