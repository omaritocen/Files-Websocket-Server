import socket
import threading

from constants import *

## Define constants

# Get the host IP address of the current machine
ADDRESS = ('', PORT)

# Setup Server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(conn, sender_address):
    print(f'[NEW CONNECTION] recieved message from {sender_address}')

    sentence = conn.recv(BUFFER_SIZE).decode()
    capitalized_sentence = sentence.upper()
    conn.send(capitalized_sentence.encode())
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
