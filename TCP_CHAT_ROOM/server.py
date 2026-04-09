import socket 
import threading 

host = 'localhost'
port = 12345
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients_sockets = []
nicknames = []

def get_nickname(client_socket):
    try:
        for client in clients_sockets:
            if client_socket == client:
                index =clients_sockets.index(client)
            return nicknames[index]
    finally:
        return "Unknown"
    
def return_socket(nickname):
    try:
        for nick in nicknames:
            index = nicknames.index(nick)
            return clients_sockets[index]
    finally:
        return 'user not connected to the server'

def broadcast(message, sender_client):
    try:
        for client in clients_sockets:
            if client != sender_client:
                client.send(message)
        
    except socket.error as e:
        print("Error occurred while broadcasting message: {}".format(e))

    finally:
        clients_sockets.remove(sender_client)
        print("connection close from client: {}".format(sender_client.getpeername()))
        sender_client.close()


def handle_client_broad(client_socket):
    try: 
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)


    except Exception as e:
        print("Error occurred while handling client: {}".format(e))
    finally:
        clients_sockets.remove(client_socket)
        print("connection close from client: {}".format(client_socket.getpeername()))
        client_socket.close()
        broadcast("{} left the chat room.".format(get_nickname(client_socket)).encode('utf-8'), client_socket)

        nickname = get_nickname(client_socket)
        if nickname in nicknames:
            nicknames.remove(nickname)


def connection_handles():
    print("Server is listening on {}:{}".format(host, port))
    while True:
        client_socket, addr = server.accept()
        print("New connection from {}:{}".format(addr[0], addr[1]))
        clients_sockets.append(client_socket)
        client_socket.send("enter your nickname".encode('utf-8'))
        data =client_socket.recv(1024).decode ('utf-8')
        nickname = data.strip()
        nicknames.append(nickname)
