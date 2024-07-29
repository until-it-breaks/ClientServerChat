import socket
import threading
import tkinter as tkt

HOST = input("Input the host server: ")
PORT = input("Input the host port: ")

if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
ENCODING = "utf8"

window = tkt.Tk()
window.title("Chat client")
messages_frame = tkt.Frame(window)
my_message = tkt.StringVar()
my_message.set("Type your messages here")
scrollbar = tkt.Scrollbar(messages_frame)

message_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
message_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
message_list.pack()
messages_frame.pack()

def receive():
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)
            message_list.insert(tkt.END, message)
        except OSError:
            break

def send(event=None):
    message = my_message.get()
    my_message.set("")
    client_socket.send(bytes(message), ENCODING)
    if message == "{quit}":
        client_socket.close()
        window.quit()

def on_closing(event=None):
    my_message.set("{quit}")
    send()

entry_text_field = tkt.Entry(window, textvariable=my_message)
entry_text_field.bind("<Return>", send)

entry_text_field.pack()
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()
window.protocol("WM_DELETE_WINDOW", on_closing)

#AF_INET refers to the ipv4 protocol, SOCK_STREAM refers to TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)

receiver_thread = threading.Thread(target=receive)
receiver_thread.start()
tkt.mainloop()