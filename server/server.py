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

def recvall(conn):
    full_request = b""
    c = 0
    while True:
        readable, writeable, exceptional = select.select([conn], [], [], 1)
        if conn in readable:
            request = conn.recv(BUFFER_SIZE)
        else: break
        if not request:
            break
        print(f"{c}: {request}")
        c += 1
        full_request += request
    full_request = full_request.decode()
    return full_request


 
def transfer_file(filename :str):
    try:
        #TODO handle file extension
        # ext = filename.split('.')[1]
        # if(ext=='jpg'):
        #    file = open(filename, "rb")
        #    return file.read()
        # else:    
        file = open(filename, "r")
        #Conditioning on file exstesnsion
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
    
    print(f'[NEW CONNECTION] recieved message from {sender_address}')
 
    # Recieve data from connection
    full_request = recvall(conn)
    print(full_request)

    # Process data
    lines = full_request.split('\r\n')
    words = lines[0].split(' ')
    request_type = words[0]
    filename = words[1].split('/')[2]
    http_type = words[2]
 
    response = ""
    if request_type == 'GET':
        file = transfer_file(filename)
        if file != -1:
            response = rg.get_response_by_verb(http_type, request_type, True, file)
             # Send data back to client
            conn.send(response)
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)
            # Send data back to client
            conn.send(response)
    else:
        data = lines[-2]
        print(data)
        receive = receive_file(filename, data)
        if receive != -1:
            response = rg.get_response_by_verb(http_type, request_type, True)
            conn.send(response.encode(FORMAT))
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)
            conn.send(response.encode(FORMAT))

 
    # Close client connection
    print(f"[CLOSE CONNECTION] client: {sender_address}")
    conn.close()


 
def start():
    server.listen(MAX_CONNECTIONS)
    print(f'[LISTENING] Server is Listening on {ADDRESS}')
    while True:
 
        # Blocking wait for user connection
        conn, sender_addrsss = server.accept()
 
        # Delegate new connection to the worker
        thread = threading.Thread(target=handle_client, args=(conn, sender_addrsss))
        thread.start()
 
        # Printing the total connections which equals to all threads - main 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
 
 
print('[STARTING] SERVER IS STARTING')
start()