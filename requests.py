import constants
import client
import os

def GET_request(fileName):  
  with open(constants.FILE_DIRECTORY + fileName, "rb") as file:
    data = file.read(constants.RECV_BUFFER_SIZE)
  
  return data

def POST_request(fileName):
  with open(client.save_path + fileName, "rb") as file:
    data = file.read(constants.RECV_BUFFER_SIZE)
  
  return data

def HEAD_request(fileName):

  try: 
    fileSize = os.path.getsize(constants.FILE_DIRECTORY + fileName)
    header = f'[HTTP/1.1 200 OK - {fileName} - {fileSize} bytes]'
    return header
  
  except:
    header = '[HTTP/1.1 404 Not Found]'
    return header


def HEAD_POST_request(fileName):

  try: 
    fileSize = os.path.getsize(client.save_path + fileName)
    header = f'[HTTP/1.1 200 OK - {fileName} - {fileSize} bytes]'
    return header
  
  except:
    header = '[HTTP/1.1 404 Not Found]'
    return header