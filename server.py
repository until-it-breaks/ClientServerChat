import socket
import threading

clients = {}
addresses = {}

HOST = ''
PORT = 53000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
ENCODING = "utf8"

#waits for incoming connections and starts a handling thread for each one
def accept_incoming_connections():
    while True:
        try:
            client, client_address = SERVER.accept()
            print("{} is connected".format(client_address))
            client.send(bytes("Hello! Please enter your name", ENCODING))
            addresses[client] = client_address
            threading.Thread(target=handle_client, args=(client,)).start()
        except OSError as e:
            print("Something went wrong when trying to estabilish a connection: {}".format(e))

def handle_client(client):
    try:
        name = client.recv(BUFFER_SIZE).decode(ENCODING)
        welcome_message = "Welcome {}, if you wish to leave the chat, type 'quit'".format(name)
        client.send(bytes(welcome_message, ENCODING))
        message = "{} has joined the chat!".format(name)
        broadcast(bytes(message, ENCODING))
        clients[client] = name
    
        #waits for inputs from the client bound to this thread and broadcasts it
        while True:
            message = client.recv(BUFFER_SIZE)
            if message != bytes("{quit}", ENCODING):
                broadcast(message, name + ": ")
            else:
                client.close()
    #Intercepts the moment the connectio is lost or whatever
    except OSError:
        if client in clients:
            client.close()
            name = clients[client]
            del clients[client]
            broadcast(bytes("{} has left the chat".format(name), ENCODING))
        


def broadcast(msg, prefix=""):
    for client in clients:
        try:
            client.send(bytes(prefix, ENCODING) + msg)
        except OSError as e:
            print("Error broadcasting to {}: {}".format(client, e))
            client.close()
            del clients[client]
            
#AF_INET refers to the ipv4 protocol, SOCK_STREAM refers to TCP
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDRESS)

SERVER.listen(5)
print("Waiting for connections")
ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join() #wait until the end of the thread before proceeding
SERVER.close()