from http import server
import socket
import threading
clients = []
blacklist = ('192.168.300.5',9999)

limiteur = threading.Semaphore(3)

def broadcast(message, _client):
    try:
        while True:
            for client in clients:
                if client != _client:
                    client.send(message.encode())
    except:
        if _client in clients:
            clients.remove(_client)
        _client.close()

def gerer_client(client, addr):
    with limiteur:
        print(f"Nouveau client connecté : {addr}")
        try:
            while True:
                data = client.recv(1024).decode()
                if not data: 
                    break

                print(f"Message reçu de {addr} : {data}")
                client.send(b"Message recu par le serveur")
        except ConnectionResetError:
            pass
        finally:
            print(f"[LOG] Déconnexion de {addr}")
            clients.remove(client)
            client.close()


def gerer_client_broadcast(client, addr):
    with limiteur:
        print(f"Nouveau client connecté : {addr}")
        try:
            while True:
                data = client.recv(1024).decode()
                if not data: 
                    break

                print(f"Message reçu de {addr} : {data}")
                broadcast(data, client)
        except ConnectionResetError:
            pass
        finally:
            print(f"[LOG] Déconnexion de {addr}")
            clients.remove(client)
            client.close()

def gerer_client_exit(client, addr):

        print(f"merci d'avoir utilisé notre serveur : {addr}votre session est terminée")
        print(f"[LOG] Déconnexion de {addr}")
        client.close()
        clients.remove(client)

def aiguillage(client, addr):
    try:
        if addr[0] in blacklist:
            print(f"[LOG] {addr[0]} est banni.")
            client.close()
            if client in clients: clients.remove(client)
            return
        
        client.settimeout(60) 
        choix = client.recv(1024).decode().strip().lower()
        client.settimeout(None) 

        if choix == "broadcast":
            gerer_client_broadcast(client, addr)
        elif "serveur" in choix:
            gerer_client(client, addr)
        elif choix == "exit":
            gerer_client_exit(client, addr)
        else:
            client.send(b"Commande inconnue.")
            client.close()
            if client in clients: clients.remove(client)
    except socket.timeout:
        print(f"[LOG] Timeout de choix pour {addr}")
        client.close()
        if client in clients: clients.remove(client)
    except:
        client.close()
        clients.remove(client)


def main():
    print("Serveur démarré sur le port 9000...")
    print("En attente de connexions...")
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(('127.0.0.1', 9000))
    serveur.listen()
    while True:
        client, addr = serveur.accept()
        clients.append(client)
        threading.Thread(target=aiguillage, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    main()