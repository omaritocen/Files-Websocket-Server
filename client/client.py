import socket

from constants import * 

# Initiate client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)

# Get sentence from user
sentence = input('Input lowercase sentence:')

# Send the message to the server
clientSocket.send(sentence.encode())


# Decode recieved socket
recieved_sentence = clientSocket.recv(BUFFER_SIZE)
decoded_sentence = recieved_sentence.decode()

# Print the result
print('From server: ', decoded_sentence)

# Close the connection
clientSocket.close()