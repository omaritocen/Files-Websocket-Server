import socket
import sys


BUFFER_SIZE = 4096
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

def process_get(route,host, protocol = 'HTTP/1.1'):
    status_line = f'GET {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    message = status_line + host_line + "\r\n"
    return message



def process_post(route, host, protocol = 'HTTP/1.1', data='to be added'):
    status_line = f'POST {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    content_type = "multipart/form-data"
    message = status_line + host_line + content_type + "\r\n"
    return message


with open('input_file.txt') as f:

    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        route = words[1]
        host = words[2]
        port = int(words[3])

        # Initiate client socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        
        if request_type == 'GET':
            get_message = process_get(route, host)
            print(get_message)
            # Send the request to the server
            clientSocket.send(get_message.encode())
            # Decode received socket

            response = clientSocket.recv(BUFFER_SIZE).decode(FORMAT)
            # Print the result
            print(response)

        elif request_type == 'POST' :
            #TODO get the data of the file and pass it to the function
            data = transfer_file(route)
            post_message = process_post(route,host, data)  
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
