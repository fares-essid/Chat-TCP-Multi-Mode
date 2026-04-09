import socket 
import threading 
import queue

messages_recus = queue.Queue()
running = True

def ecouter_serveur(client):
    """Thread qui écoute les messages du serveur"""
    global running
    try:
        while running:
            try:
                reponse = client.recv(1024).decode()
                if not reponse:
                    break
                messages_recus.put(reponse)
            except socket.timeout:
                continue
    except Exception as e:
        if running:
            print(f"\n[ERREUR] Connexion perdue: {e}")
    finally:
        running = False


def set_nickname(client):
    """Envoie le nickname au serveur"""
    nickname = input("Entrez votre nickname : ")
    # CORRECTION: encode() AVANT send()
    client.send(nickname.encode())
        

def demande_saisie():
    """Demande une commande à l'utilisateur"""
    # CORRECTION: Simplifié - retourne juste la string
    return input("Entrez votre commande (serveur/broadcast/client/exit) : ")


def comm_client_client(socket_client):
    """Gère la communication client-to-client"""
    socket_client.send("client".encode())
    
    try:
        # CORRECTION: Ajout de timeout pour éviter les freezes
        instruction = messages_recus.get(timeout=5)
        print(f"[SERVEUR] {instruction}")
        
        nom = input("Nom du destinataire : ")
        socket_client.send(nom.encode())
        
        try:
            instruction2 = messages_recus.get(timeout=5)
            print(f"[SERVEUR] {instruction2}")
        except queue.Empty:
            print("[ERREUR] Pas de réponse du serveur")
            return
        
        if "n'est pas en ligne" in instruction2 or "timeout" in instruction2.lower():
            print("[INFO] L'utilisateur n'est pas disponible")
        else:
            message = input("Message : ")
            socket_client.send(message.encode())
            
    except queue.Empty:
        print("[ERREUR] Pas de réponse du serveur (timeout)")


def choix(client):
    """Gère le menu des choix de communication"""
    try:
        while True:
            # CORRECTION: Utilise demande_saisie() directement
            commande = demande_saisie().lower().strip()
            
            if commande == "exit" or commande == "":
                print("Déconnexion demandée.")
                client.send("exit".encode())
                break
            
            elif commande == "broadcast":
                client.send("broadcast".encode())
                print("\n[MODE BROADCAST] (Tapez 'exit' pour quitter)")
                while True:
                    msg = input("Message à diffuser : ")
                    if msg.lower() == "exit":
                        break
                    client.send(msg.encode())
                    # CORRECTION: Utilise la queue au lieu de recv() directe
                    try:
                        reponse = messages_recus.get(timeout=5)
                        print(f"Serveur : {reponse}")
                    except queue.Empty:
                        print("[INFO] Message envoyé")
                    
            elif commande == "serveur":
                client.send("serveur".encode())
                print("\n[MODE SERVEUR] (Tapez 'exit' pour quitter)")
                while True:
                    msg = input("Vous : ")
                    if msg.lower() == "exit":
                        print("Fin de la conversation.")
                        break
                    client.send(msg.encode())
                    # CORRECTION: Utilise la queue au lieu de recv() directe
                    try:
                        reponse = messages_recus.get(timeout=5)
                        print(f"Serveur : {reponse}")
                    except queue.Empty:
                        print("[INFO] Message envoyé")
                        
            elif commande == "client":
                comm_client_client(client)
            else:
                print("[ERREUR] Commande inconnue. Essayez: serveur, broadcast, client, exit")

    except ConnectionResetError:
        print("\n[ERREUR] Le serveur a fermé la connexion.")
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        
    finally:
        print("\nDéconnexion du serveur...")
        client.close()


def main():
    global running
    
    # Connexion au serveur
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 9000))
        print("✓ Connecté au serveur")
    except Exception as e:
        print(f"✗ Impossible de se connecter au serveur: {e}")
        return

    # Démarrer le thread d'écoute
    thread_ecoute = threading.Thread(target=ecouter_serveur, args=(client,), daemon=True)
    thread_ecoute.start()

    print("--- Connecté au serveur (Tapez 'exit' pour quitter) ---\n")
    
    try:
        while running:
            # CORRECTION: Ajout de timeout pour éviter les freezes infinis
            try:
                instruction = messages_recus.get(timeout=5)
                print(instruction)
                
                # Vérification plus flexible des instructions du serveur
                if "bienvenue" in instruction.lower() and "nickname" in instruction.lower():
                    set_nickname(client)
                    
                elif "choix" in instruction.lower() or "choisissez" in instruction.lower():
                    choix(client)
                else:
                    print(f"[INFO] {instruction}")
                    
            except queue.Empty:
                # Timeout normal, continue la boucle
                continue
    
    except ConnectionResetError:
        print("\n[ERREUR] Le serveur a fermé la connexion.")
    except KeyboardInterrupt:
        print("\n[INFO] Déconnexion...")
    except Exception as e:
        print(f"\n[ERREUR] {e}")
    finally:
        running = False
        client.close()
        print("Vous êtes déconnecté.")

if __name__ == "__main__":
    main()
