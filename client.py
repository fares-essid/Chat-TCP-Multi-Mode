import socket 
import threading 
import time
import sys
import queue

messages_recus = queue.Queue()

my_nickname = {"nickname": None}
partage = {"choix": None}

running = True

def ecouter_serveur(client):
    global running
    try:
        while running:
            reponse = client.recv(1024).decode()
            if not reponse:
                break
            messages_recus.put(reponse)
    except:
        if running: print("\n[ERREUR] Connexion perdue.")
    finally:
        running = False


def set_nickname(client):
    nickname= input("donner votre nickname")
    client.send(nickname.encode())
        

def demande_saisie(partage):
    try:
        while partage["choix"] == None:
            partage["choix"] = input("Entrez votre commande : ")
        return partage
        
    except  EOFError:
        print("Aucune donnée reçue du serveur.")
        pass

def comm_client_client(socket_client):
    socket_client.send("client_to_client".encode())
    instruction = messages_recus.get() 
    print(f"[SERVEUR] {instruction}")
    nom = input("Nom du destinataire : ")
    socket_client.send(nom.encode())
    instruction2 = messages_recus.get()
    print(f"[SERVEUR] {instruction2}")
    if "[LOG] Timeout de choix de nickname à contacter pour" in instruction2:
        print("timeout")
    else:
        message = input("Message : ")
        socket_client.send(message.encode())

def choix(client):
    try :
        while True :
            partage["choix"] = None
            partage["choix"]=demande_saisie(partage)

            commande = partage["choix"].lower().strip()
            if commande == "exit" or commande == "":
                print("Déconnexion demandée.")
                client.send("exit".encode())
                break
            
            
            elif commande == "broadcast":
                client.send(commande.encode())
                while True:
                    msg = input("Message à diffuser : ")
                    client.send(msg.encode())
                    print(f"Serveur : {client.recv(1024).decode()}")
                    
            
            elif commande == "serveur":
                client.send(commande.encode())
                while True:
                    msg = input("Vous : ")
                    if msg.lower() == "exit":
                        print("Fin de la conversation.")
                        break
                    client.send(msg.encode())
                    print(f"Serveur : {client.recv(1024).decode()}")
            elif commande == "client":
                comm_client_client(client)

    except ConnectionResetError:
        print("Le serveur a fermé la connexion.")
        
    finally:
        print("Déconnexion du serveur...")
        client.close()


def main():
    global running
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 9000))
    except:
        print("Impossible de se connecter au serveur.")
        return

    thread_ecoute = threading.Thread(target=ecouter_serveur, args=(client,), daemon=True)
    thread_ecoute.start()

    print("--- Connecté au serveur (Tapez 'exit' pour quitter) ---")
    try:
        while True:
            instruction = messages_recus.get() 
            print(instruction)
            if instruction.lower()=="Bienvenue sur le serveur !entrez votre nickname :":
                set_nickname(client)
            
            elif instruction.lower()=="choix de communication":
               choix(client)
            else:
                print(f"\n[INFO] {instruction}")
    
    except ConnectionResetError:
        print("Le serveur a fermé la connexion.")

if __name__ == "__main__":
    main()


