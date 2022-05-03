import socket

from constants import * 

# Read GET/POST requests from input file 
with open('input_file.txt') as f:
    requests = []
    for line in f:
        requests.append(line)

# Initiate client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)

# Declaring GET/POST Requests
GET = requests[0]
POST = requests[1]

# Send the request to the server
clientSocket.send(GET.encode())


# Decode recieved socket
recieved_sentence = clientSocket.recv(BUFFER_SIZE)
decoded_sentence = recieved_sentence.decode()

# Print the result
print('From server: ', decoded_sentence)

# Close the connection
clientSocket.close()