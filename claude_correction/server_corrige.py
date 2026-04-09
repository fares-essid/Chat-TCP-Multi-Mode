import socket
import threading

clients = []
nicknames = []
blacklist = ('192.168.30.5',)  # IP valide (sans le port en tuple)

limiteur = threading.Semaphore(16)

def get_nickname(client_socket):
    """Récupère le nickname d'un client"""
    try:
        for i, client in enumerate(clients):
            if client_socket == client:
                return nicknames[i]
        return "Unknown"
    except:
        return "Unknown"
    
def return_socket(nickname):
    """Retourne le socket d'un client par son nickname"""
    try:
        if nickname in nicknames:
            index = nicknames.index(nickname)
            return clients[index]
        return None
    except:
        return None

def broadcast(message, _client):
    """Envoie un message à tous les clients sauf l'expéditeur"""
    try:
        for client in clients:
            if client != _client:
                client.send(message.encode())
    except:
        if _client in clients:
            clients.remove(_client)
        _client.close()

def gerer_client(client, addr):
    """Gère la communication client-serveur simple"""
    with limiteur:
        print(f"[SERVEUR] Client connecté : {addr}")
        try:
            while True:
                data = client.recv(1024).decode()
                if not data: 
                    break

                print(f"[MESSAGE] De {addr} : {data}")
                client.send(b"Message recu par le serveur")
        except ConnectionResetError:
            pass
        except Exception as e:
            print(f"[ERREUR] {e}")
        finally:
            print(f"[LOG] Déconnexion de {addr}")
            if client in clients:
                clients.remove(client)
            mon_nickname = get_nickname(client)
            if mon_nickname != "Unknown" and mon_nickname in nicknames:
                nicknames.remove(mon_nickname)
            client.close()


def gerer_client_broadcast(client, addr):
    """Gère la communication en broadcast"""
    with limiteur:
        print(f"[BROADCAST] Client connecté : {addr}")
        try:
            while True:
                data = client.recv(1024).decode()
                if not data: 
                    break

                print(f"[BROADCAST] De {addr} : {data}")
                broadcast(data, client)
        except ConnectionResetError:
            pass
        except Exception as e:
            print(f"[ERREUR] {e}")
        finally:
            print(f"[LOG] Déconnexion de {addr}")
            if client in clients:
                clients.remove(client)
            mon_nickname = get_nickname(client)
            if mon_nickname != "Unknown" and mon_nickname in nicknames:
                nicknames.remove(mon_nickname)
            client.close()

def gerer_client_exit(client, addr):
    """Ferme la connexion d'un client"""
    print(f"[EXIT] Merci d'avoir utilisé notre serveur : {addr}")
    print(f"[LOG] Déconnexion de {addr}")
    
    if client in clients:
        clients.remove(client)
    
    mon_nickname = get_nickname(client)
    if mon_nickname != "Unknown" and mon_nickname in nicknames:
        nicknames.remove(mon_nickname)
    
    client.close()

        
def set_nickname(client_socket):
    """Demande et enregistre le nickname du client"""
    try:
        client_socket.send("Bienvenue sur le serveur ! Entrez votre nickname :".encode())
        client_socket.settimeout(30)
        client_nickname = client_socket.recv(1024).decode().strip()
        client_socket.settimeout(None)
        
        if client_nickname:
            client_socket.send(f"Bienvenue {client_nickname} !".encode())
            nicknames.append(client_nickname)
            print(f"[NICKNAME] {client_socket.getpeername()} -> {client_nickname}")
        else:
            client_socket.send("Nickname vide. Connexion fermée.".encode())
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)

    except socket.timeout:  
        print(f"[LOG] Timeout de nickname pour {client_socket.getpeername()}")
        client_socket.send("Temps écoulé pour choisir un nickname. Connexion fermée.".encode())
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)
    except Exception as e:
        print(f"[ERREUR] {e}")
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)
        
def choisir_nickname_a_contacter(client_socket):
    """Demande au client le nickname de son destinataire"""
    try:
        client_socket.send("Entrez le nickname du client à contacter :".encode())
        client_socket.settimeout(30)
        nickname_a_contacter = client_socket.recv(1024).decode().strip()  
        client_socket.settimeout(None)
        
        if nickname_a_contacter in nicknames:
            index = nicknames.index(nickname_a_contacter)
            return clients[index]
        else:
            msg = f"L'utilisateur {nickname_a_contacter} n'est pas en ligne."
            client_socket.send(msg.encode())
            return None
            
    except socket.timeout:
        print(f"[LOG] Timeout de choix de nickname à contacter pour {client_socket.getpeername()}")
        client_socket.send("Temps écoulé pour choisir un nickname à contacter. Connexion fermée.".encode())
        mon_nickname = get_nickname(client_socket)
        if client_socket in clients:
            clients.remove(client_socket)
        if mon_nickname != "Unknown" and mon_nickname in nicknames:
            nicknames.remove(mon_nickname)
        client_socket.close()
    except Exception as e:
        print(f"[ERREUR] {e}")
        client_socket.close()
            
def client_to_client(client_sender, client_recv):
    """Gère la communication directe entre deux clients"""
    with limiteur:
        print(f"[CLIENT-TO-CLIENT] {client_sender.getpeername()} -> {client_recv.getpeername()}")
        try:
            while True:
                data_env_recv = client_sender.recv(1024).decode()
                if not data_env_recv:
                    break
                else : 
                    print(f"[C2C] De {client_sender.getpeername()} : {data_env_recv}")
                    client_recv.send(data_env_recv.encode())
        except ConnectionResetError:
            pass
        except Exception as e:
            print(f"[ERREUR] {e}")
        finally:
            print(f"[LOG] Déconnexion de {client_sender.getpeername()}")
            if client_sender in clients:
                clients.remove(client_sender)
            mon_nickname = get_nickname(client_sender)
            if mon_nickname != "Unknown" and mon_nickname in nicknames:
                nicknames.remove(mon_nickname)
            client_sender.close()

def demander_choix(client):
    """Demande au client quel type de communication il veut"""
    try:
        msg = "Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :"
        client.send(msg.encode())
        client.settimeout(60) 
        choix = client.recv(1024).decode().strip().lower()
        client.settimeout(None) 
        
        if choix:
            return choix
        else :
            client.send("Pas de choix enregistré.".encode())
            return None
            
    except socket.timeout:
        print(f"[LOG] Timeout de choix pour {client.getpeername()}")
        client.send("Temps écoulé. Connexion fermée.".encode())
        if client in clients:
            clients.remove(client)
        mon_nickname = get_nickname(client)
        if mon_nickname != "Unknown" and mon_nickname in nicknames:
            nicknames.remove(mon_nickname)
        client.close()
        return None
    except Exception as e:
        print(f"[ERREUR] {e}")
        return None


def aiguillage(client, addr):
    """Route le client vers le bon type de communication"""
    try:
        # Vérifier blacklist
        if addr[0] in blacklist:
            print(f"[LOG] {addr[0]} est banni.")
            client.close()
            if client in clients:
                clients.remove(client)
            return
        
        # Demander nickname
        set_nickname(client)
        
        # Boucle de communication
        while True:
            choix = demander_choix(client)
            
            if choix is None:
                break
            
            if "serveur" in choix:
                gerer_client(client, addr)
                break

            elif "client" in choix:
                client_recv = choisir_nickname_a_contacter(client)
                if client_recv:
                    client_to_client(client, client_recv)
                    break

            elif choix == "broadcast":
                gerer_client_broadcast(client, addr)
                break
                
            elif choix == "exit":
                gerer_client_exit(client, addr)
                break
            else:
                client.send(b"Commande inconnue.")
                
    except socket.timeout:
        print(f"[LOG] Timeout pour {addr}")
        if client in clients:
            clients.remove(client)
        client.close()
    except Exception as e:
        print(f"[ERREUR] Erreur aiguillage: {e}")
        if client in clients:
            clients.remove(client)
        client.close()


def main():
    print("="*50)
    print("Serveur démarré sur le port 9000...")
    print("En attente de connexions...")
    print("="*50)
    
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(('127.0.0.1', 9000))
    serveur.listen(5)
    
    try:
        while True:
            client, addr = serveur.accept()
            print(f"\n[CONNEXION] Nouveau client : {addr}")
            clients.append(client)
            threading.Thread(target=aiguillage, args=(client, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SERVEUR] Arrêt du serveur...")
        serveur.close()
    except Exception as e:
        print(f"[ERREUR] {e}")
        serveur.close()

if __name__ == "__main__":
    main()
