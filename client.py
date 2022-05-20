import socket

import constants
import os
import requests

save_path = 'C:/Users/samue/OneDrive/Escritorio/clientFiles/'

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

    loop = True

    while loop:
                              
        if (command_to_send[0] == constants.GET):

            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            header = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive header
            print(header)

            if header != '[HTTP/1.1 404 Not Found]':
                filename = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive filename
                completeName = os.path.join(save_path, filename)
                
                with open(completeName, "wb") as file:

                    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE) #receive data
                    file.write(data_received)
            else:
                pass

            #print('Press enter to continue')
            #newLine = input()
            #print(newLine)
#--------------------------------------------------------------------------------------

        elif (command_to_send[0] == constants.POST):
            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            header = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive header
            print(header)

            if header != '[HTTP/1.1 404 Not Found]':
                filename = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive filename
                completeName = os.path.join(constants.FILE_DIRECTORY, filename)
                
                with open(completeName, "wb") as file:

                    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE) #receive data
                    file.write(data_received)
            else:
                pass
#--------------------------------------------------------------------------------------

        elif (command_to_send[0] == constants.HEAD):
            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            header = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive header
            print(header)
#--------------------------------------------------------------------------------------

        elif (command_to_send[0] == constants.DELETE):
            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            header = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive header
            response = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive response
            print(header)
            print(response)
#--------------------------------------------------------------------------------------


        elif command_to_send[0] == constants.QUIT:
            client_socket.send(bytes(' '.join(command_to_send), constants.ENCONDING_FORMAT))
            header = client_socket.recv(constants.RECV_BUFFER_SIZE).decode(constants.ENCONDING_FORMAT) #receive header
            print(header)
            print('Closing connection.....')
            client_socket.close()  
            loop = False
            break

        else:
            print('Please input a valid command...')

        print('Commands: GET, POST, HEAD, DELETE')
        print('Input command:')
        command_to_send = input().split()


if __name__ == '__main__':
    main()