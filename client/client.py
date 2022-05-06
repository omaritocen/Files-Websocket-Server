import socket


BUFFER_SIZE = 2048

# TODO: DELETE
SERVER_IP = '10.0.0.101' # My LAN IP
PORT = 5505
SERVER_ADDRESS = (SERVER_IP, PORT)

def get_server_address():
    with open('input_file.txt') as f:
        for line in f:
            words = line.split(" ", 3)
            server_ip = words[2]
            port = words[3]
            break
        return server_ip,port

def process_get(filename,server_ip_address):
    message = 'GET /files/{0} HTTP/1.1\nHost: {1}'.format(filename,server_ip_address)
    return message



def process_post(filename,server_ip_address,data='to be added'):
    #TODO calculate content length and content type if needed
    message = 'POST /files/{0} HTTP/1.1\nHost: {1}\nContent-Length:\nContent-Type:\n\nData'.format(filename,server_ip_address)
    return message


# Read Server Address from input file 
server_ip,port = get_server_address()
server_address = (server_ip,port)

# Initiate client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(server_address)


with open('input_file.txt') as f:

    for line in f:
        words = line.split(" ", 3)
        request_type = words[0]
        filename = words[1]
        server_address = (server_ip, port)
        if(request_type == 'GET'):
            get_message = process_get(filename,server_ip)
            # Send the request to the server
            clientSocket.send(get_message.encode())
        else :
            #TODO get the data of the file and pass it to the function
            post_message = process_post(filename,server_ip)  
            # Send the request to the server
            clientSocket.send(post_message.encode())




# Decode recieved socket
recieved_sentence = clientSocket.recv()
decoded_sentence = recieved_sentence.decode()

# Print the result
print('From server: ', decoded_sentence)

# Close the connection
clientSocket.close()