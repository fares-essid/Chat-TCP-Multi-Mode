def choix(client):
    try :
        while True :
            partage["choix"] = None
            thread_input = threading.Thread(target=demande_saisie, args=(partage,), daemon=True)
            thread_input.start()
            timedeb=time.time()
            innactivité=False

            while partage["choix"] is None:
                if time.time() - timedeb > 60:
                    innactivité = True
                    break
                time.sleep(0.1) 
                
            if innactivité:
                print("\n60 secondes d'inactivité. Fermeture...")
                break

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
                    thread_input.join()
                    
            
            elif commande == "serveur":
                client.send(commande.encode())
                while True:
                    msg = input("Vous : ")
                    if msg.lower() == "exit":
                        print("Fin de la conversation.")
                        break
                    client.send(msg.encode())
                    print(f"Serveur : {client.recv(1024).decode()}")

    except ConnectionResetError:
        print("Le serveur a fermé la connexion.")
        
    finally:
        print("Déconnexion du serveur...")
        client.close()