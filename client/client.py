import socket
import sys

BUFFER_SIZE = 4096
FORMAT = "utf-8"


def recvall():
    full_request = b""
    while True:
        request = clientSocket.recv(BUFFER_SIZE)
        if not request:
            break
        full_request += request
    return full_request


def transfer_file(filename):
    try:
        ext = filename.split('.')[1]
        if ext == 'jpg' or ext == 'png':
            file = open(filename, "rb")
            return file.read()
        else:
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
        file = open(filename, "wb")
        file.write(data)
    except IOError as e:
        print(f"IOError: {e}")
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")


def process_get(route, host, protocol='HTTP/1.1'):
    status_line = f'GET {route} {protocol}\r\n'
    host_line = f'Host: {host}'
    message = status_line + host_line + "\r\n"
    return message


def process_post(route, host, file_size, protocol='HTTP/1.1', ):
    status_line = f'POST {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    content_length = f'Content-Length: {file_size}\r\n'
    message = status_line + host_line + content_length + "\r\n"
    return message


with open('input_file.txt') as f:
    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        route = words[1]
        host = words[2]
        port = int(words[3])
        filename = route.split('/')[-1]

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
            header_data_split = full_response.split(b"\r\n")

            # Process data
            lines = full_response.split(b"\r\n")
            data = lines[2]

            headers = lines[0].decode()
            words = headers.split(' ')
            http_type = words[0]
            status_code = words[1]
            status_message = words[2]
            receive_file(filename, data)


        elif request_type == 'POST':

            data = transfer_file(filename)
            file_size = len(data)
            header = process_post(route, host, file_size)
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
