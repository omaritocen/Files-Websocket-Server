import socket
import sys
import gzip

BUFFER_SIZE = 4096
FORMAT = "utf-8"

request_cache = {}

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def recvall(conn, ext):
    request = conn.recv(BUFFER_SIZE)
    lines = request.split(b"\r\n")
    content_length_line = [x for x in lines if x.startswith(b'Content-Length')]
    content_encoding_line = [x for x in lines if x.startswith(b'Content-Encoding')]
    content_length = int(content_length_line[0].split(b" ")[1].decode())
    header_body_split = request.split(b"\r\n")
    status_code = header_body_split[0].split(b" ")[1].decode()
    print(header_body_split[0].decode())
    if(status_code != '200'):
        return -1

    body = header_body_split[-1]
    test = request.split(b"\r\n\r\n")
    if(test is not None and len(test) > 1):
        body = test[-1]
    # print(body)
    remaining_content = content_length - len(body)
    headers_length = len(header_body_split[0] + header_body_split[1])
    if content_length >= BUFFER_SIZE - headers_length or body == b'' and status_code == '200':
        while True:
            request = conn.recv(BUFFER_SIZE)
            if not request:
                break
            body += request

            remaining_content -= len(request)
            # print(remaining_content)
            if remaining_content <= 0:
                break
    if(len(content_encoding_line) > 0):
        if(content_encoding_line[0].split(b" ")[1].decode() == 'gzip'):
            body = gzip.decompress(body)
    return body, header_body_split[0]


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
 
 
def process_get(route, host, protocol='HTTP/1.0'):
    status_line = f'GET {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    encoding = "Accept-Encoding: gzip, deflate, br\r\n"
    message = status_line + host_line + encoding + "\r\n"
    return message
 
 
def process_post(route, host, file_size, protocol='HTTP/1.0', ):
    status_line = f'POST {route} {protocol}\r\n'
    host_line = f'Host: {host}\r\n'
    content_length = f'Content-Length: {file_size}\r\n'
    message = status_line + host_line + content_length + "\r\n"
    return message

def get_filename_if_exists(route):
    try:
        f_name = route.split('/')[-1]
        return f_name
    except:
        return ""

def open_connection(host):
    isIp = validate_ip(host)
    if not isIp:
        host_ip = socket.gethostbyname(host)
    else:
        host_ip = host
    # Initiate client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host_ip, port))

    return clientSocket


with open('input_file.txt') as f:
    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        route = words[1]
        host = words[2]
        port = 80
        if len(words) == 4:
            port = int(words[3])
        filename = route.split('/')[-1]
        

        if request_type == 'GET':
            get_message = process_get(route, host)
            # request_if_exists = get_filename_if_exists(route)
            if get_message != "":
                if get_message in request_cache:
                    # filename = filename_if_exists
                    print("Found File name in cache no need to get it from the server")
                    print(request_cache[get_message].decode())
                else:
                    
                    clientSocket = open_connection(host)
                    # Send the request to the server
                    clientSocket.sendall(get_message.encode(FORMAT))
                    # Decode received socket
                    data , response = recvall(clientSocket, filename.split(".")[-1])
                    request_cache[get_message] = response
                    receive_file(filename, data)

        elif request_type == 'POST':
            
            clientSocket = open_connection(host)
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