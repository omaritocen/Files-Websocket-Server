from ntpath import join
import socket
import threading
import sys
import response_generation as rg

# DEFINE CONSTANTS
MAX_CONNECTIONS = 5
PORT = 5505
BUFFER_SIZE = 2048
FORMAT = "utf-8"

# Setup Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname("localhost")
ADDRESS = (HOST, PORT)
server.bind(ADDRESS)
print(server.getsockname())


def transfer_file(filename):
    try:
        file = open(filename, "r")
        return file.read()    
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
    request = conn.recv(BUFFER_SIZE).decode()

    # Process data
    lines = request.split('\r\n')
    words = lines[0].split(' ')

    request_type = words[0]
    filename = words[1].split('/')[2]
    http_type = words[2]

    # print(request_type)
    # print(http_type)

    response = ""
    if request_type == 'GET':
        file = transfer_file(filename)

        if file != -1:
            response = rg.get_response_by_verb(http_type, request_type, True, file)
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)
    else:
        data = lines[-1][6:]
        receive = receive_file(filename, data)
        if receive != -1:
            response = rg.get_response_by_verb(http_type, request_type, True)
        else:
            response = rg.get_response_by_verb(http_type, request_type, False)

    # Send data back to client
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
