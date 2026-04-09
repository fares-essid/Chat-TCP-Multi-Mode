# 💬 Chat TCP Multi-Mode

Un système de chat TCP en Python permettant la communication entre clients et serveur avec plusieurs modes de communication : serveur-client, client-to-client et broadcast.

---

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Démarrer le serveur](#démarrer-le-serveur)
  - [Démarrer un client](#démarrer-un-client)
  - [Modes de communication](#modes-de-communication)
- [Architecture](#architecture)
- [Structure du code](#structure-du-code)
- [Gestion des erreurs](#gestion-des-erreurs)
- [Troubleshooting](#troubleshooting)
- [Améliorations futures](#améliorations-futures)
- [Licence](#licence)

---

## 👀 Vue d'ensemble

Ce projet implémente un serveur TCP multithreadé qui gère plusieurs clients simultanément. Chaque client peut choisir entre trois modes de communication :

1. **Mode Serveur** : Communication directe avec le serveur
2. **Mode Broadcast** : Envoi de messages à tous les autres clients
3. **Mode Client** : Communication directe avec un autre client spécifique

### Architecture globale

```
                        ┌──────────────────┐
                        │   SERVEUR TCP    │
                        │   Port 9000      │
                        └──────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
            ┌────────┐      ┌────────┐      ┌────────┐
            │Client 1│      │Client 2│      │Client 3│
            │(Alice) │      │(Bob)   │      │(Carol) │
            └────────┘      └────────┘      └────────┘
```

---

## ✨ Fonctionnalités

### ✅ Implémentées

- **Authentification par nickname** : Chaque client doit choisir un nickname unique
- **Mode serveur** : Conversations avec le serveur central
- **Mode broadcast** : Messages diffusés à tous les clients connectés (sauf l'expéditeur)
- **Mode client-to-client** : Communication directe et privée entre deux clients
- **Gestion des timeouts** : Protection contre les connexions bloquées
- **Blacklist d'IP** : Permet de bannir certaines adresses IP
- **Multithreading** : Support de 16 connexions simultanées (configurable)
- **Gestion des exceptions** : Fermeture propre des connexions
- **Messages de log** : Traçabilité complète des événements

### 🔮 Fonctionnalités disponibles

- Sauvegarde de l'historique des conversations
- Chiffrement des messages
- Base de données pour les comptes utilisateurs
- Interface graphique (GUI)
- Support de fichiers (partage de fichiers)

---

## 🛠️ Prérequis

- **Python** 3.6 ou supérieur
- Système d'exploitation : Windows, macOS, ou Linux
- Pas de dépendances externes (utilise les modules standards Python)

### Vérifier votre version Python

```bash
python --version
# ou
python3 --version
```

---

## 📦 Installation

### 1. Cloner ou télécharger le projet

```bash
# Via git
git clone <url-du-repo>
cd chat-tcp

# Ou télécharger les fichiers directement
```

### 2. Structure des fichiers

```
chat-tcp/
├── server_corrige.py      # Serveur TCP
├── client_corrige.py      # Client TCP
├── README.md              # Ce fichier
└── CORRECTIONS_COMPLETES.md # Historique des corrections
```

### 3. Vérifier les permissions

Sur Linux/macOS, assurez-vous que les fichiers sont exécutables :

```bash
chmod +x server_corrige.py
chmod +x client_corrige.py
```

---

## 🚀 Utilisation

### Démarrer le serveur

```bash
# Terminal 1 - Démarrer le serveur
python server_corrige.py
# ou
python3 server_corrige.py
```

**Résultat attendu :**
```
==================================================
Serveur démarré sur le port 9000...
En attente de connexions...
==================================================
```

Le serveur écoute sur `127.0.0.1:9000` (localhost, port 9000)

### Démarrer un client

Dans un autre terminal :

```bash
# Terminal 2 - Démarrer le premier client
python client_corrige.py
```

**Résultat attendu :**
```
✓ Connecté au serveur
--- Connecté au serveur (Tapez 'exit' pour quitter) ---

Bienvenue sur le serveur ! Entrez votre nickname :
```

Entrez votre nickname (ex: `Alice`)

```
Bienvenue Alice !
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
```

Répétez pour un 2e client (Terminal 3) avec un autre nickname (ex: `Bob`)

---

## 💬 Modes de communication

### Mode 1️⃣ : Serveur

Permet une conversation directe avec le serveur.

```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> serveur

[MODE SERVEUR] (Tapez 'exit' pour quitter)
Vous : Bonjour le serveur!
Serveur : Message recu par le serveur
Vous : exit
Fin de la conversation.
```

**Utilisation :**
- Entrez vos messages
- Le serveur reçoit et répond
- Tapez `exit` pour quitter ce mode

---

### Mode 2️⃣ : Broadcast

Envoie un message à **tous les autres clients** connectés.

**Terminal 1 (Alice) :**
```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> broadcast

[MODE BROADCAST] (Tapez 'exit' pour quitter)
Message à diffuser : Bonjour tout le monde!
Message envoyé
```

**Terminal 2 (Bob) reçoit automatiquement :**
```
Bonjour tout le monde!
```

**Points importants :**
- Les messages sont envoyés à **tous SAUF l'expéditeur**
- Pas de confirmation de lecture
- Tapez `exit` pour quitter ce mode

---

### Mode 3️⃣ : Client-to-Client

Communication directe et privée entre deux clients.

**Terminal 1 (Alice) :**
```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> client

[SERVEUR] Entrez le nickname du client à contacter :
Nom du destinataire : Bob
[SERVEUR] (En attente de Bob...)
Message : Salut Bob, ça va?
```

**Terminal 2 (Bob) reçoit :**
```
Salut Bob, ça va?
```

**Points importants :**
- Le destinataire DOIT être en ligne et avoir un nickname valide
- Si l'utilisateur n'existe pas, vous recevrez un message d'erreur
- La communication est **directe et privée**
- Timeout de 30 secondes pour choisir le destinataire

---

## Mode 4️⃣ : Exit

Ferme la connexion du client.

```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> exit

Déconnexion demandée.
Déconnexion du serveur...
Vous êtes déconnecté.
```

**Serveur affiche :**
```
[EXIT] Merci d'avoir utilisé notre serveur : ('127.0.0.1', 54321)
[LOG] Déconnexion de ('127.0.0.1', 54321)
```

---

## 🏗️ Architecture

### Composants principaux

```
┌─────────────────────────────────────────────────────────┐
│                      SERVEUR                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  • Gestion des clients (liste + nicknames)             │
│  • Semaphore (limiter à 16 clients simultanés)         │
│  • Blacklist d'IP                                       │
│                                                         │
│  Threads de gestion :                                   │
│  • set_nickname() - Authentification                    │
│  • gerer_client() - Mode serveur                        │
│  • gerer_client_broadcast() - Mode broadcast            │
│  • client_to_client() - Mode client-client              │
│  • demander_choix() - Menu de sélection                 │
│  • aiguillage() - Routage des clients                   │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      CLIENT                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Thread principal :                                     │
│  • main() - Connexion et boucle principale             │
│                                                         │
│  Thread secondaire :                                    │
│  • ecouter_serveur() - Écoute les messages (queue)    │
│                                                         │
│  Fonctions UI :                                         │
│  • set_nickname() - Choix du nickname                   │
│  • demande_saisie() - Input utilisateur                │
│  • choix() - Menu de sélection                         │
│  • comm_client_client() - Mode client-client            │
│                                                         │
│  Queue :                                                │
│  • messages_recus - Buffer thread-safe des messages    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Flux de communication

```
CLIENT                           SERVEUR
  │                                 │
  ├─── connect('127.0.0.1:9000) ──>│
  │                                 │
  │<── "Entrez votre nickname" ────│
  │                                 │
  ├─── nickname ────────────────────>│
  │                                 ├─ Enregistre nickname
  │<── "Bienvenue Alice!" ─────────│
  │                                 │
  │<── "Choisissez un mode" ────────│
  │                                 │
  ├─── "broadcast" ─────────────────>│
  │                                 ├─ Diffuse à tous
  │<── Message d'Alice ─────────────│ (sauf Alice)
  │                                 │
  ├─── "exit" ──────────────────────>│
  │                                 ├─ Ferme la connection
  │<── Déconnexion ────────────────│
  │                                 │
```

---

## 📂 Structure du code

### Serveur (`server_corrige.py`)

| Fonction | Description |
|----------|-------------|
| `get_nickname(client_socket)` | Récupère le nickname d'un client |
| `return_socket(nickname)` | Retourne le socket d'un client par son nickname |
| `broadcast(message, _client)` | Envoie un message à tous les clients sauf l'expéditeur |
| `gerer_client(client, addr)` | Gère la communication mode serveur |
| `gerer_client_broadcast(client, addr)` | Gère la communication en broadcast |
| `gerer_client_exit(client, addr)` | Ferme proprement une connexion |
| `set_nickname(client_socket)` | Authentification du client |
| `choisir_nickname_a_contacter(client_socket)` | Demande le destinataire en mode client-client |
| `client_to_client(client_sender, client_recv)` | Gère la communication client-client |
| `demander_choix(client)` | Affiche le menu et reçoit le choix |
| `aiguillage(client, addr)` | Route le client vers le bon mode |
| `main()` | Boucle principale du serveur |

### Client (`client_corrige.py`)

| Fonction | Description |
|----------|-------------|
| `ecouter_serveur(client)` | Thread d'écoute - reçoit les messages |
| `set_nickname(client)` | Envoie le nickname au serveur |
| `demande_saisie()` | Demande l'entrée utilisateur |
| `comm_client_client(socket_client)` | Gère le mode client-client |
| `choix(client)` | Menu principal et sélection du mode |
| `main()` | Initialisation et boucle principale |

---

## ⚠️ Gestion des erreurs

Le projet gère les erreurs suivantes :

### Erreurs réseau

```python
# Serveur ne répond pas
✗ Impossible de se connecter au serveur.

# Connexion perdue
[ERREUR] Connexion perdue: ...
```

### Erreurs de timeout

```python
# Timeout pour choisir un nickname (30s)
[LOG] Timeout de nickname pour 127.0.0.1

# Timeout pour choisir le destinataire (30s)
[LOG] Timeout de choix de nickname à contacter pour 127.0.0.1

# Timeout pour répondre au serveur (5s)
[ERREUR] Pas de réponse du serveur (timeout)
```

### Erreurs de validation

```python
# Utilisateur non trouvé
L'utilisateur Bob n'est pas en ligne.

# Nickname vide
Nickname vide. Connexion fermée.

# Commande inconnue
[ERREUR] Commande inconnue. Essayez: serveur, broadcast, client, exit
```

### Blacklist d'IP

```python
# IP bannie
[LOG] 192.168.30.5 est banni.
```

---

## 🔧 Troubleshooting

### ❌ "Connection refused"

**Symptôme :** `✗ Impossible de se connecter au serveur`

**Solutions :**
1. Vérifiez que le serveur est lancé
2. Vérifiez que le serveur écoute sur `127.0.0.1:9000`
3. Vérifiez qu'aucun pare-feu ne bloque le port 9000
4. Sur Linux/macOS : vérifiez avec `netstat -an | grep 9000`

```bash
# Linux/macOS - Vérifier le port
netstat -an | grep 9000
lsof -i :9000

# Windows - Vérifier le port
netstat -ano | findstr :9000
```

---

### ❌ "Address already in use"

**Symptôme :** `OSError: [Errno 48] Address already in use`

**Solutions :**
1. Un serveur tourne déjà sur le port 9000
2. Attendez 30-60 secondes et réessayez (TIME_WAIT)
3. Arrêtez l'ancien processus

```bash
# Linux/macOS - Tuer le processus
lsof -ti :9000 | xargs kill -9

# Windows - Tuer le processus
taskkill /PID <PID> /F
```

---

### ❌ Client se déconnecte immédiatement

**Symptôme :** `[ERREUR] Connexion perdue.`

**Solutions :**
1. Vérifiez les logs du serveur
2. Vérifiez votre nickname (pas vide)
3. Vérifiez votre connexion réseau
4. Relancez client et serveur

---

### ❌ Freeze ou blocage du programme

**Symptôme :** Rien ne se passe, le programme est bloqué

**Solutions :**
1. C'est normal pendant les timeouts (max 5-60 secondes)
2. Appuyez sur `Ctrl+C` pour forcer l'arrêt
3. Vérifiez la queue de messages du serveur
4. Redémarrez client/serveur

```bash
# Forcer l'arrêt du programme
Ctrl + C
```

---

### ❌ Messages qui ne s'affichent pas

**Symptôme :** Vous recevez un message mais ne le voyez pas immédiatement

**Solutions :**
1. C'est normal en mode serveur (attendez votre tour)
2. En broadcast, l'expéditeur ne voit PAS son propre message
3. Attendez que le serveur réponde
4. Vérifiez votre nickname avec `@nick`

---

## 🎯 Cas d'usage

### Exemple 1 : Chat simple serveur-client

```bash
# Terminal 1 - Serveur
$ python server_corrige.py
Serveur démarré sur le port 9000...

# Terminal 2 - Client Alice
$ python client_corrige.py
✓ Connecté au serveur
Bienvenue sur le serveur ! Entrez votre nickname :
> Alice
Bienvenue Alice !
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> serveur
[MODE SERVEUR]
Vous : Bonjour!
Serveur : Message recu par le serveur
Vous : exit
```

### Exemple 2 : Broadcast entre 3 clients

```bash
# Terminal 1 - Serveur
# Terminal 2 - Alice (broadcast)
> broadcast
Message à diffuser : Bonjour tout le monde!

# Terminal 3 - Bob reçoit
Bonjour tout le monde!

# Terminal 4 - Carol reçoit
Bonjour tout le monde!
```

### Exemple 3 : Communication privée

```bash
# Terminal 2 - Alice
> client
Nom du destinataire : Bob
Message : Salut Bob!

# Terminal 3 - Bob reçoit
Salut Bob!
```

---

## 📊 Statistiques du projet

- **Lignes de code (serveur)** : ~280
- **Lignes de code (client)** : ~210
- **Fonctions (serveur)** : 12
- **Fonctions (client)** : 6
- **Threads utilisés** : 2 par client
- **Clients max simultanés** : 16 (configurable)
- **Ports utilisés** : 1 (9000)
- **Dépendances externes** : 0

---

## 🚀 Améliorations futures

### Haute priorité
- [ ] Sauvegarde de l'historique des messages
- [ ] Authentification par mot de passe
- [ ] Gestion des groupes/channels
- [ ] Commandes spéciales (like `/list`, `/info`)

### Moyenne priorité
- [ ] Chiffrement des messages (SSL/TLS)
- [ ] Interface graphique (PyQt/Tkinter)
- [ ] Support des fichiers (transfert de fichiers)
- [ ] Base de données (SQLite)
- [ ] Configuration externe (config.json)

### Basse priorité
- [ ] API REST pour clients externes
- [ ] Notifications desktop
- [ ] Emojis et Unicode avancé
- [ ] Thèmes UI personnalisés
- [ ] Analytics et statistiques

---

## 📝 Contrôle de version

### Version 1.0 (Actuelle)
- ✅ 3 modes de communication
- ✅ Gestion des timeouts
- ✅ Blacklist d'IP
- ✅ Multithreading
- ✅ Gestion des exceptions

### Version 0.9 (Précédente)
- ❌ Bugs majeurs (13 erreurs corrigées)
- ❌ Race conditions
- ❌ Freeze du programme

---

## 🐛 Bugs corrigés

Voir `CORRECTIONS_COMPLETES.md` pour la liste détaillée des 13 bugs corrigés.

### Bugs majeurs corrigés
1. `.send().encode()` → `.send(encode())`
2. Boucle infinie dans broadcast
3. Race conditions (deux threads sur un socket)
4. Freezes infinis (.get() sans timeout)
5. Retour de dictionnaire au lieu de string

---

## 📞 Support

### Besoin d'aide?

1. Consultez la section [Troubleshooting](#troubleshooting)
2. Vérifiez `CORRECTIONS_COMPLETES.md` pour les erreurs
3. Examinez les logs du serveur et du client
4. Relancez les programmes avec `-v` (à implémenter)

### Signaler un bug

Incluez :
- Votre système d'exploitation
- Version Python
- Les messages d'erreur exacts
- Les étapes pour reproduire le bug

---

## 📄 Licence

Ce projet est fourni à titre d'exemple pédagogique.

Libre d'utilisation, modification et distribution.

---

## 👨‍💻 Crédits

Projet développé comme exercice d'apprentissage en Python.

**Concepts utilisés :**
- Sockets TCP
- Multithreading
- Queues thread-safe
- Gestion des timeouts
- Communication réseau

---

## 📚 Ressources utiles

### Documentation officielle
- [Python socket module](https://docs.python.org/3/library/socket.html)
- [Python threading module](https://docs.python.org/3/library/threading.html)
- [Python queue module](https://docs.python.org/3/library/queue.html)

### Tutoriels
- [Real Python - Socket Programming](https://realpython.com/python-sockets/)
- [Real Python - Threading](https://realpython.com/intro-to-python-threading/)

### Outils de diagnostic
```bash
# Vérifier les ports ouverts
netstat -an | grep LISTEN

# Vérifier les processus Python
ps aux | grep python

# Tester la connexion
telnet 127.0.0.1 9000
```

---

## ✨ Conseils d'utilisation

### Pour les développeurs

1. **Déboguer facilement**
   ```bash
   # Lancer avec stdout
   python -u client_corrige.py
   ```

2. **Tester plusieurs clients**
   ```bash
   # Terminal 1
   python server_corrige.py
   
   # Terminal 2, 3, 4... (multiple clients)
   python client_corrige.py
   ```

3. **Monitorer le serveur**
   - Observez les logs `[LOG]`
   - Vérifiez les messages `[ERREUR]`
   - Comptez les clients connectés

### Pour les utilisateurs

1. **Choisissez un nickname unique** pour éviter les collisions
2. **Utilisez le broadcast** pour les annonces publiques
3. **Utilisez client-client** pour les conversations privées
4. **Tapez 'exit'** pour vous déconnecter proprement

---

## 🎓 Apprentissages clés

En étudiant ce code, vous apprendrez :

✅ Comment créer un serveur TCP multithreadé
✅ Comment gérer plusieurs clients simultanément
✅ Comment éviter les race conditions
✅ Comment utiliser les queues pour la synchronisation
✅ Comment gérer les timeouts et erreurs réseau
✅ Comment structurer un projet Python

---

**Amusez-vous bien avec votre chat TCP! 🎉**

Pour toute question, consultez les logs ou relancez les programmes. 🚀
