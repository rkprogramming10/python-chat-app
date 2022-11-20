
# starting part

from email import message
from http import server
from ipaddress import ip_address
import socket

from threading import Thread
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address, port))
server.listen()

clients = []
print('server is running.....')
list_of_clients = []
nickname_list = []


def client_thread(conn, nickname):
    conn.send('Welcome to this chatroom! '.encode())
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print(message)
                broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def remove_nickname(nickname):
    if nickname in nickname_list:
        nickname_list.remove(nickname)


while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode())
    nickname = conn.recv(2048).decode()

    list_of_clients.append(conn)
    nickname_list.append(nickname)
    message = nickname + ' has joined the chat'
    print(nickname + ' connected')
    broadcast(message, conn)

    new_thread = Thread(target=client_thread, args=(conn, nickname))
    new_thread.start()

# Ending of the server part
