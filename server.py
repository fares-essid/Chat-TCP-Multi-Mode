from http import client, server
import socket
import threading
clients = []
nicknames = []
blacklist = ('192.168.30.5',9999)

limiteur = threading.Semaphore(16)

def get_nickname(client_socket):
    try:
        for client in clients:
            if client_socket == client:
                index =clients.index(client)
            return nicknames[index]
    finally:
        return "Unknown"
    
def return_socket(nickname):
    try:
        for nick in nicknames:
            index = nicknames.index(nick)
            return clients[index]
    finally:
        return 'user not connected to the server'

def broadcast(message, _client):
    try:
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

        
def set_nickname(client_socket):
        try:
            client_socket.send("Bienvenue sur le serveur !entrez votre nickname :").encode()
            client_socket.settimeout(30)
            client_nickname = client_socket.recv(1024).decode().strip()
            client_socket.settimeout(None)
            client_socket.send(f"Bienvenue {client_nickname} !".encode())
            nicknames.append(client_nickname)

        except socket.timeout:  
            print(f"[LOG] Timeout de nickname pour {client_socket.getpeername()}")
            client_socket.send("Temps écoulé pour choisir un nickname. Connexion fermée.").encode()
            client_socket.close()
            if client_socket in clients: clients.remove(client_socket)
        
def choisir_nickname_a_contacter(client_socket):
    try:
        client_socket.send("Entrez le nickname du client à contacter :").encode()
        client_socket.settimeout(30)
        nickname_a_contacter = client_socket.recv(1024).decode().strip()  
        client_socket.settimeout(None)
        if nickname_a_contacter in nicknames:
            index=nicknames.index(nickname_a_contacter)
            return clients[index]
        else:
            client_socket.send("l'utilisateur {} n'est pas en ligne.".format(nickname_a_contacter).encode())
            return None
    except socket.timeout:
        print(f"[LOG] Timeout de choix de nickname à contacter pour {client_socket.getpeername()}")
        client_socket.send("Temps écoulé pour choisir un nickname à contacter. Connexion fermée.").encode()
        client_socket.close()
        mon_nickname=get_nickname(client_socket)
        if client_socket in clients: clients.remove(client_socket)
        if mon_nickname in nicknames: nicknames.remove(mon_nickname)
            
def client_to_client(client_sender,client_recv):
    with limiteur:
        print(f"le client_sender avec ip {client_sender.getpeername()} veut envoyer un message à {client_recv.getpeername()}")
        try:
            while True:
                data_env_recv= client_sender.recv(1024).decode()
                if not data_env_recv:
                    break
                else : 
                    print(f"Message reçu de {client_sender.getpeername()} : {data_env_recv}")
                    client_recv.send(data_env_recv.encode())
        except ConnectionResetError:
            pass
        finally:
            print(f"[LOG] Déconnexion de {client_sender.getpeername()}")
            clients.remove(client_sender)
            client_sender.close()

def demander_choix(client):
    try:
        client.send("choix de communication".encode())
        client.settimeout(60) 
        choix = client.recv(1024).decode().strip().lower()
        client.settimeout(None) 
        if choix:
            return choix
        else :
            client.send("pas de choix a ete enregistré").encode()
    except socket.timeout:
            print(f"[LOG] Timeout de choix de nickname à contacter pour {client.getpeername()}")
            client.send("Temps écoulé pour choisir un nickname à contacter. Connexion fermée.").encode()
            clients.remove(client)
            nickname=get_nickname(client)
            nicknames.remove(nickname)
            client.close()



def aiguillage(client, addr):
    try:
        if addr[0] in blacklist:
            print(f"[LOG] {addr[0]} est banni.")
            client.close()
            if client in clients: clients.remove(client)
            return
        set_nickname(client)
        while True:
            choix= demander_choix(client)
            if "serveur" in choix:
                gerer_client(client, addr)  

            if "client" in choix:
                client_recv = choisir_nickname_a_contacter(client)
                if client_recv:
                    client_to_client(client, client_recv)

            elif choix == "broadcast":
                gerer_client_broadcast(client, addr)
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