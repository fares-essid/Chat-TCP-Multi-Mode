import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 8080))
clients = []
server.listen(10)
limiter = threading.Semaphore(3)


def broadcast(message, _client):
    try:
        for client in clients:
            if client != _client:
                client.send(message).encode()
    except:
        if _client in clients:
            clients.remove(_client)
        _client.close()

def gerer_client(client, addr):
    with limiter:
        print(f"Nouveau client connecté : {addr}")
        while True:
            try:    
                message= client.recv(1024).decode()
                if message:
                    print(f"Message reçu: {message}")
                    broadcast(message, client)
            except:
                if client in clients: 
                    clients.remove(client)
                print(f"[LOG] {addr} a quitté le chat.")
                client.close()
def main():
    print("Serveur de diffusion démarré sur le port 8080...")  
    print("En attente de clients...")             
    while True:
        client ,addr =server.accept()
        clients.append(client)
        client.send(b"Welcome to the server!")
        thread = threading.Thread(target=gerer_client, args=(client,addr))
        thread.start()

    


                