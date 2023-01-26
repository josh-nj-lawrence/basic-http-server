"""
    Implementation of a simple HTTP/1.0 Server
"""

import socket

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8765

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print("Listening on port {}".format(SERVER_PORT))

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Parse the HTTP headers
    headers = request.split('\n')
    filename = headers[0].split()[1]
    
    if filename == '/':
        filename = '/index.html'
    try:
        # Get index.html content
        fle = open("." + filename)
        content = fle.read()
        fle.close()

        # Send HTTP response
        response = 'HTTP/1.0 200 OK\n\n' + content

    except FileNotFoundError:
            response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found"

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()