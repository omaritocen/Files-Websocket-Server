import socket
from tokenize import String
import sys


BUFFER_SIZE = 2048
FORMAT = "utf-8"

def transfer_file(filename):
    try:
        file = open(filename, "r")
        return file.read().encode(FORMAT)
    except FileNotFoundError:
        print(f"{filename} doesn't exist")
    except IOError as e:
        print(f"IOError: {e}")
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")

def receive_file(filename, data):
    try:
        file = open(filename, "w")
        file.write(data.decode(FORMAT))
    except IOError as e:
        print(f"IOError: {e}")
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")

def get_server_address():
    with open('input_file.txt') as f:
        for line in f:
            words = line.split(" ", 3)
            server_ip = words[2]
            port = words[3]
            break
        return server_ip, int(port)

def process_get(filename,server_ip_address):
    message = 'GET /files/{0} HTTP/1.1\nHost: {1}\r\n'.format(filename,server_ip_address)
    return message



def process_post(filename,server_ip_address,data='to be added'):
    #TODO calculate content length and content type if needed
    message = 'POST /files/{0} HTTP/1.1\r\nHost: {1}\r\nContent-Length:\nContent-Type:\r\nData: {2}\r\n'.format(filename,server_ip_address, data)
    return message


# Read Server Address from input file 
server_ip,port = get_server_address()
server_address = (server_ip,port)


with open('input_file.txt') as f:

    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        filename = words[1]

        # Initiate client socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(server_address)
        
        if request_type == 'GET':
            get_message = process_get(filename,server_ip)
            # Send the request to the server
            clientSocket.send(get_message.encode())
            # Decode received socket
            respone = clientSocket.recv(BUFFER_SIZE).decode(FORMAT)
            # Print the result
            print(respone)

        elif request_type == 'POST' :
            #TODO get the data of the file and pass it to the function
            data = transfer_file(filename)
            post_message = process_post(filename,server_ip, data)  
            # Send the request to the server
            clientSocket.send(post_message.encode(FORMAT))
            # Decode received socket
            received_sentence = clientSocket.recv(BUFFER_SIZE)
            decoded_sentence = received_sentence.decode()

            # Print the result
            print(decoded_sentence)

        print('')
        print('------------------------------------')



clientSocket.close()
print('[CLIENT PROCESS ENDED]')

# Close the connection
