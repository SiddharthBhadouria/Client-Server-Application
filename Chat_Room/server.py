import socket
from threading import Thread

# dictionary to store information about the client
addresses = {}
clients = {}

host = '127.0.0.1'
port = 8080


# creating a server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

# broadcast function to broadcast the message to all the clients
def broadcast(msg, prefix = ""):
    for i in clients:
        i.send(bytes(prefix, 'UTF-8') + msg)

# function to connect the clients to the server 
def client_connections():
    while True:
        connection, address = server.accept() # accepting the connection to server
        print(address, " has connected!")   
        connection.send("Welcome to our Chat room\nPlease type in your name to continue".encode('UTF-8'))
        addresses[connection] = address     # storing the connection and address to the dictionary
        Thread(target=handle_client, args= (connection, address)).start()       # creating a thread 

# function to handle the clients connected to the server
def handle_client(connection, address):

    # receive the name of the client
    clientName = connection.recv(1024).decode('UTF-8')
    welcome = "Welcome "+clientName+ "Type #quit to quit the chat room."
    connection.send(bytes(welcome, 'UTF-8'))

    # broadcasting the msg to all the servers
    msg = clientName + " has joined the chat room"
    broadcast(bytes(msg, 'UTF-8'))

    # adding to dictionary
    clients[connection] = clientName

    # reading the messages of the client until the user types "#quit"
    while True:
        msg = connection.recv(1024)
        if msg != bytes("#quit", 'UTF-8'):
            broadcast(msg, clientName + ": ")
        else:
            connection.send(bytes("#quit", "UTF-8"))
            connection.close()

            # deleting the client from the dictionary of clients
            del clients[connection]
            broadcast(bytes(clientName + " has left the chat room!", 'UTF-8'))




if __name__ == "__main__":
    server.listen(5)
    print("Server is ready to connect!")
    t1 = Thread(target=client_connections)
    t1.start()
    t1.join()
