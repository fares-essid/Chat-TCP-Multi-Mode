from http import server
import socket
import threading

def gerer_client(client, addr):
    print(f"Nouveau client connecté : {addr}")
    while True:
        data = client.recv(1024).decode()
        if not data: break
        
        client.send(b"Message recu par le serveur")
    client.close()

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('0.0.0.0', 9000))
serveur.listen()

while True:
    client, addr = serveur.accept()
    thread = threading.Thread(target=gerer_client, args=(client, addr))
    thread.start()

