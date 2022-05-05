import socket


BUFFER_SIZE = 2048

# TODO: DELETE
SERVER_IP = '10.0.0.101' # My LAN IP
PORT = 5505
SERVER_ADDRESS = (SERVER_IP, PORT)

# Initiate client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)

# Get sentence from user
sentence = input('Input lowercase sentence:')

# Send the message to the server
clientSocket.send(sentence.encode())


# Decode recieved socket
recieved_sentence = clientSocket.recv()
decoded_sentence = recieved_sentence.decode()

# Print the result
print('From server: ', decoded_sentence)

# Close the connection
clientSocket.close()