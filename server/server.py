from distutils import extension
import socket
import threading
import sys
import response_generation as rg
import select

# DEFINE CONSTANTS
MAX_CONNECTIONS = 5
PORT = 5505
BUFFER_SIZE = 4096
FORMAT = "utf-8"

# Setup Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname("localhost")
ADDRESS = (HOST, PORT)
server.bind(ADDRESS)
print(server.getsockname())


def handle_get(filename, http_type, request_type, conn):
    file = transfer_file(filename)
    if file != -1:
        response = rg.get_response_by_verb(http_type, request_type, True, file)
    else:
        response = rg.get_response_by_verb(http_type, request_type, False)
    # Send data back to client
    conn.send(response)


def handle_post(header_lines, headers, ext, filename, http_type, request_type, conn):
    content_length_line = [x for x in header_lines if x.startswith(b'Content-Length')]
    content_length = int(content_length_line[0].split(b" ")[1].decode())
    remaining_content = content_length - len(headers[1])
    body = headers[1]
    headers_length = len(headers[0])
    if content_length >= BUFFER_SIZE - headers_length:
        while True:
            request = conn.recv(BUFFER_SIZE)
            if not request:
                break
            body += request
            remaining_content -= BUFFER_SIZE
            if remaining_content <= 0:
                break
    # handle images
    if ext == "jpg" or ext == "png":
        image = body
        receive = receive_file(filename, image)
        if receive != -1:
            response = rg.get_response_by_verb(http_type, request_type, True)
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)
    # handle txt and html
    else:
        data = body.decode()
        receive = receive_file(filename, data)
        if receive != -1:
            response = rg.get_response_by_verb(http_type, request_type, True)
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)
    conn.send(response.encode(FORMAT))


def recvall(conn):
    request = conn.recv(BUFFER_SIZE)

    headers = request.split(b"\r\n\r\n")
    header_lines = headers[0].split(b"\r\n")

    status_line = header_lines[0].decode().split(" ")
    request_type = status_line[0]
    filename = status_line[1].split('/')[-1]
    ext = filename.split(".")[1]
    http_type = status_line[2]

    if http_type == 'HTTP/1.1':
        # conn.settimeout(10)
        # while True:
        #     if not request:
        #         break
            # IN CASE OF GET
            if request_type == 'GET':
                handle_get(filename, http_type, request_type, conn)
            # IN CASE OF POST
            else:
                handle_post(header_lines, headers, ext, filename, http_type, request_type, conn)

    elif http_type == 'HTTP/1.0':
        # IN CASE OF GET
        if request_type == 'GET':
            handle_get(filename, http_type, request_type, conn)
        # IN CASE OF POST
        else:
            handle_post(header_lines, headers, ext, filename, http_type, request_type, conn)


def transfer_file(filename: str):
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
        return -1
    except IOError as e:
        print(f"IOError: {e}")
        return -1
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")
        return -1


def receive_file(filename, data):
    try:
        ext = filename.split('.')[1]
        if ext == 'jpg' or ext == 'png':
            file = open(filename, "wb")
            file.write(data)
        else:
            file = open(filename, "w")
            file.write(data)
            return 0
    except IOError as e:
        print(f"IOError: {e}")
        return -1
    except:
        print(f"Unexpected Error: {sys.exc_info()[0]}")
        return -1


def handle_client(conn, sender_address):
    print(f'[NEW CONNECTION] received message from {sender_address}')
    # Recieve data from connection
    recvall(conn)
    # Close client connection
    print(f"[CLOSE CONNECTION] client: {sender_address}")
    conn.close()


def start():
    server.listen(MAX_CONNECTIONS)
    print(f'[LISTENING] Server is Listening on {ADDRESS}')
    while True:
        # Blocking wait for user connection
        conn, sender_address = server.accept()

        # Delegate new connection to the worker
        thread = threading.Thread(target=handle_client, args=(conn, sender_address))
        thread.start()

        # Printing the total connections which equals to all threads - main 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print('[STARTING] SERVER IS STARTING')
start()
