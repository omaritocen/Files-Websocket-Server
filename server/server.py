import socket
import threading

# DEFINE CONSTANTS
MAX_CONNECTIONS = 5
PORT = 5505
BUFFER_SIZE = 2048

# Setup Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = ('', PORT)
server.bind(ADDRESS)


def handle_client(conn, sender_address):
    print(f'[NEW CONNECTION] recieved message from {sender_address}')

    # Recieve data from connection
    sentence = conn.recv(BUFFER_SIZE).decode()

    # Process data
    capitalized_sentence = sentence.upper()

    # Send data back to client
    conn.send(capitalized_sentence.encode())

    # Close client connection
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
