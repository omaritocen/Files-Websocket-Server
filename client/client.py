import select
import socket
import sys


BUFFER_SIZE = 4096
FORMAT = "utf-8"

def recvall():
    full_request = b""
    c = 0
    while True:
        request = clientSocket.recv(BUFFER_SIZE)
        if not request:
            break
        print(f"{c}: {request}")
        c += 1
        full_request += request
    full_request = full_request.decode()
    return full_request
    

def transfer_file(filename):
    try:
        #TODO handle file extension
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
        file.write(data)
    except IOError as e:
        print(f"IOError: {e}")
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")



def process_get(route,host, protocol = 'HTTP/1.1'):
    status_line = f'GET {route} {protocol}\r\n'
    host_line = f'Host: {host}'
    message = status_line + host_line + "\r\n"
    return message



def process_post(route, host, protocol = 'HTTP/1.1'):
    status_line = f'POST {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    # content_type = "multipart/form-data"
    message = status_line + host_line + "\r\n"
    return message


with open('input_file.txt') as f:

    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        route = words[1]
        host = words[2]
        port = int(words[3])
        filename = route.split('/')[2]
        # Initiate client socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))

        
        if request_type == 'GET':
            get_message = process_get(route, host)
            print(get_message)
            # Send the request to the server
            clientSocket.send(get_message.encode(FORMAT))
            # Decode received socket

            full_response = recvall()
            print(full_response)

            # Process data
            lines = full_response.split('\r\n')
            words = lines[0].split(' ')
            http_type = words[0]
            status_code = words[1]
            status_message = words[2]
            data = lines[-2]
            receive = receive_file(filename, data)


        elif request_type == 'POST' :
            
            data = transfer_file(filename)
            header = process_post(route,host)
            post_message = header.encode(FORMAT) + data + b"\r\n"
            # Send the request to the server

            clientSocket.sendall(post_message)
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
