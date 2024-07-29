import socket
import threading

clients = {}
addresses = {}

HOST = ''
PORT = 53000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
ENCODING = "utf8"

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDRESS)

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