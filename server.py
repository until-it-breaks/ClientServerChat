import socket
import threading

clients = {}
addresses = {}

HOST = ''
PORT = 53000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
ENCODING = "utf8"

#AF_INET refers to the ipv4 protocol, SOCK_STREAM refers to TCP
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDRESS)

#waits for incoming connections and starts a handling thread for each one
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("{} is connected".format(client_address))
        client.send(bytes("Hello! Type your name and press Enter!", ENCODING))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFFER_SIZE).decode(ENCODING)
    welcome_message = "Welcome {}, if you wish to leave the chat, type {quit}".format(name)
    client.send(bytes(welcome_message, ENCODING))
    message = "{} has joined the chat!".format(name)
    broadcast(bytes(message, ENCODING))
    clients[client] = name

    #waits for inputs from the client bound to this thread and broadcasts it
    while True:
        message = client.recv(BUFFER_SIZE)
        if message != bytes("{quit}", ENCODING):
            broadcast(bytes(message, name + ": "))
        else:
            client.send(bytes("{quit}", ENCODING))
            client.close()
            del clients[client]
            broadcast(bytes("{} has left the chat".format(name), ENCODING))
            break

def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, ENCODING) + msg)

SERVER.listen(5)
print("Waiting for connections")
ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join() #wait until the end of the thread before proceeding
SERVER.close()