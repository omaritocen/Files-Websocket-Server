import socket
import threading
import sys
import response_generation as rg

# DEFINE CONSTANTS
MAX_CONNECTIONS = 5
PORT = 5505
BUFFER_SIZE = 4096
FORMAT = "utf-8"
number_of_connections = 0

# Setup Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname("localhost")
ADDRESS = (HOST, PORT)
server.bind(ADDRESS)
print(server.getsockname())


# def create_child_thread():
    
def recvall(conn, is_main_client_thread: bool, sender_address):
    print("New Thread Started for Client: {}".format(sender_address))
    persistent_connection = False
    thread = None
    with conn:
        if is_main_client_thread:
            conn.settimeout(5)
        while True:
            try: 
                try:
                    request = conn.recv(BUFFER_SIZE)
                except socket.error:
                    break
                if request:
                    thread = threading.Thread(target=recvall, args=(conn, False, sender_address))
                    thread.start()
                    # print(request)
                    # print("No request recieved, closing client connection...")
                    # conn.close()
                    # break
                    
                    headers = request.split(b"\r\n\r\n")
                    header_lines = headers[0].split(b"\r\n")

                    status_line = header_lines[0].decode().split(" ")
                    request_type = status_line[0]
                    filename = status_line[1].split('/')[-1]
                    ext = filename.split(".")[1]
                    http_type = status_line[2]
                
                    
                    #Check if http is presistent or not
                    if http_type == 'HTTP/1.1' and persistent_connection == False:
                        persistent_connection = True
                        print("HTTP/1.1 Setitng timeout to close...")
                        print("We are in persistent connection")    
                        
                    # IN CASE OF GET
                    if request_type == 'GET':
                        file = transfer_file(filename)
                        if file != -1:
                            response = rg.get_response_by_verb(http_type, request_type, True, file)
                        else:
                            response = rg.get_response_by_verb(http_type, request_type, False)
                        # Send data back to client
                        conn.send(response)
                    # IN CASE OF POST
                    else:
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
                        thread.kill()
                        
                    if http_type == 'HTTP/1.0':
                        print("HTTP/1.0 Closing client connection...")
                        conn.close()
                        break
                else:
                    conn.close()
                    break       
            except socket.timeout:
                print("Connection timeout reached (5 seconds), closing client socket...")
                thread.kill()
                conn.close()
                break   
           


def transfer_file(filename: str):
    try:
        ext = filename.split('.')[1]
        if ext == 'jpg' or ext == 'png':
            file = open(filename, "rb")
            data = file.read()
            file.close()
            return data
        else:
            file = open(filename, "r")
            data = file.read().encode(FORMAT)
            file.close()
            return data
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
            file.close()
        else:
            file = open(filename, "w")
            file.write(data)
            file.close()
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
    recvall(conn, True, sender_address)
    # conn.close()
    print(f"[CLOSE CONNECTION] client: {sender_address}")
  


def start():
    number_of_connections = 0
    server.listen(MAX_CONNECTIONS)
    print(f'[LISTENING] Server is Listening on {ADDRESS}')
    while True:
        # Blocking wait for user connection
        conn, sender_address = server.accept()
        # Delegate new connection to the worker
        thread = threading.Thread(target=handle_client, args=(conn, sender_address))
        thread.start()
        number_of_connections +=1

        # Printing the total connections which equals to all threads - main 
        print(f"[ACTIVE CONNECTIONS] {number_of_connections}")


print('[STARTING] SERVER IS STARTING')
start()
