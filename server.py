import socket
import threading
import constants
import requests
import os

# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = constants.IP_SERVER

def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    
# Handler for manage incomming clients conections...

def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)
        remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(command)

#--------------------------------------------------------------------------------------

        if (command == constants.GET):
            header = requests.HEAD_request(remote_command[1])

            if header != '[HTTP/1.1 404 Not Found]':
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
                client_connection.sendall(remote_command[1].encode(constants.ENCONDING_FORMAT)) #send file name
                data = requests.GET_request(remote_command[1]) #send data
                client_connection.sendall(data)
            
            else:
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
#--------------------------------------------------------------------------------------

        elif (command == constants.POST):
            header = requests.HEAD_POST_request(remote_command[1])

            if header != '[HTTP/1.1 404 Not Found]':
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
                client_connection.sendall(remote_command[1].encode(constants.ENCONDING_FORMAT)) #send file name
                data = requests.POST_request(remote_command[1]) #send data
                client_connection.sendall(data)
            
            else:
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
#--------------------------------------------------------------------------------------

        elif (command == constants.HEAD):
            header = requests.HEAD_request(remote_command[1])
            client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
#--------------------------------------------------------------------------------------

        elif (command == constants.DELETE):
            header = requests.HEAD_request(remote_command[1])

            if header != '[HTTP/1.1 404 Not Found]':
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
                os.remove(constants.FILE_DIRECTORY + remote_command[1])
                client_connection.sendall('File deleted'.encode(constants.ENCONDING_FORMAT)) #send response
            
            else:
                client_connection.sendall(header.encode(constants.ENCONDING_FORMAT)) #send header
                client_connection.sendall('File not deleted'.encode(constants.ENCONDING_FORMAT)) #send response
#--------------------------------------------------------------------------------------
        
        elif (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            is_connected = False
            

        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

#Function to start server process...
def server_execution():
    tuple_connection = (server_address,constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()