import constants
import client

def GET_request(fileName):  
  with open(constants.FILE_DIRECTORY + fileName, "rb") as file:
    data = file.read(constants.RECV_BUFFER_SIZE)
  
  return data

def POST_request(fileName):
  with open(client.save_path + fileName, "rb") as file:
    data = file.read(constants.RECV_BUFFER_SIZE)
  
  return data
  