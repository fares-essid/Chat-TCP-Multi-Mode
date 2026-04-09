# 🏗️ ARCHITECTURE & CONFIGURATION

## Architecture générale

```
┌────────────────────────────────────────────────────────────────┐
│                        INTERNET LAYER                          │
├────────────────────────────────────────────────────────────────┤
│  Protocol: TCP/IP
│  Ports: 9000 (listening)
│  Address: 127.0.0.1 (localhost)
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                           │
├────────────────────────────────────────────────────────────────┤
│
│  ┌─────────────────────────────────────────────────────────┐
│  │              SERVEUR TCP (server_corrige.py)           │
│  ├─────────────────────────────────────────────────────────┤
│  │                                                         │
│  │  DATA STRUCTURES:                                       │
│  │  • clients[] - Liste de tous les sockets connectés     │
│  │  • nicknames[] - Liste des nicknames correspondants    │
│  │  • blacklist = ('192.168.30.5',) - IPs bannies        │
│  │  • limiteur = Semaphore(16) - Limite 16 clients max   │
│  │                                                         │
│  │  MAIN THREAD:                                           │
│  │  │                                                      │
│  │  ├─ bind('127.0.0.1', 9000)                           │
│  │  ├─ listen(5) - Backlog de 5 connexions               │
│  │  └─ accept() ─── Crée un nouveau thread client        │
│  │                                                         │
│  │  CLIENT THREADS (un par client connecté):             │
│  │  │                                                      │
│  │  ├─ set_nickname() ─── Auth + enregistrement          │
│  │  │                                                      │
│  │  ├─ aiguillage() ─── Routeur principal                │
│  │  │   │                                                  │
│  │  │   ├─ blacklist check ─── Bannir si bloqué         │
│  │  │   │                                                  │
│  │  │   └─ while True:                                    │
│  │  │       ├─ demander_choix() ─── Menu                 │
│  │  │       │                                              │
│  │  │       ├─ "serveur" ─ gerer_client()               │
│  │  │       ├─ "broadcast" ─ gerer_client_broadcast()   │
│  │  │       ├─ "client" ─ choisir_nickname_a_contacter() │
│  │  │       │            ─ client_to_client()            │
│  │  │       └─ "exit" ─ gerer_client_exit()             │
│  │  │                                                      │
│  │  └─ Nettoyage final ─── Fermer socket + nettoyer    │
│  │                                                         │
│  └─────────────────────────────────────────────────────────┘
│
└────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
┌──────────────────────────┬──────────────────────────┬───────────┐
│   CLIENT 1 (ALICE)       │   CLIENT 2 (BOB)        │ CLIENT N  │
├──────────────────────────┼──────────────────────────┼───────────┤
│                          │                          │           │
│ THREADS:                 │ THREADS:                 │ THREADS:  │
│ 1. Main thread           │ 1. Main thread           │ 1. Main   │
│    └─ choix()            │    └─ choix()            │    └─ UI  │
│                          │                          │           │
│ 2. Listen thread         │ 2. Listen thread         │ 2. Listen │
│    └─ ecouter_serveur()  │    └─ ecouter_serveur()  │    └─ RX  │
│                          │                          │           │
│ DATA STRUCTURES:         │ DATA STRUCTURES:         │ DATA:     │
│ • my_nickname            │ • my_nickname            │ • socket  │
│ • messages_recus Queue   │ • messages_recus Queue   │ • queue   │
│ • running flag           │ • running flag           │ • run     │
│                          │                          │           │
└──────────────────────────┴──────────────────────────┴───────────┘
```

---

## Flux de données

### 1. Connexion initiale

```
CLIENT                          SERVEUR
  │                               │
  ├─ socket() ─────────────────>  │
  │                               │
  ├─ connect() ─────────────────> ├─ accept()
  │                               │ ├─ append(client)
  │                               │ └─ spawn_thread()
  │                               │
  │<─ "Entrez nickname" ────────┤ ├─ set_nickname()
  │                               │
  ├─ input("nickname") ──────────>│
  │                               │ ├─ recv(nickname)
  │                               │ └─ append(nicknames)
  │<─ "Bienvenue Alice!" ────────┤
  │                               │
  │<─ "Choisissez mode" ─────────┤ ├─ aiguillage()
  │                               │
```

### 2. Mode Serveur (Server Mode)

```
CLIENT                          SERVEUR
  │                               │
  ├─ send("serveur") ───────────> │ ├─ if "serveur" in choix
  │                               │ │  ├─ gerer_client()
  │                               │ │  │  ├─ recv() → Message
  │                               │ │  │  └─ send() → Réponse
  ├─ send("Bonjour") ───────────>│
  │                               │ └─ "Message reçu par le serveur"
  │<─ "Message reçu..." ────────┤
  │                               │
```

### 3. Mode Broadcast

```
CLIENT1(Alice)     SERVER         CLIENT2(Bob)    CLIENT3(Carol)
  │                  │               │               │
  ├─ "broadcast" ──>│               │               │
  │                 │ ├─ broadcast()│               │
  │                 │ │             │               │
  ├─ "Coucou!" ────>│ │             |               │
  │                 │ ├──────────────> recv()       │
  │                 │ ├──────────────────────────> recv()
  │                 │                 │               │
  │                 │                 Affiche        Affiche
  │                 │                 "Coucou!"      "Coucou!"
  │                 │                 │               │
```

### 4. Mode Client-to-Client

```
CLIENT1(Alice)     SERVER          CLIENT2(Bob)
  │                  │                │
  ├─ "client" ─────>│                │
  │                 │ ├─ ask nickname│
  │<─ "Nickname?" ──┤                │
  ├─ "Bob" ────────>│                │
  │                 │ ├─ find(Bob)   │
  │                 │ ├─ client_to_client()
  │                 │ │              │
  │<─ Ready ────────┤                │
  ├─ "Salut Bob!" ──────────────────> recv()
  │                 │                │
  │                 │             Affiche
  │                 │             "Salut Bob!"
  │                 │                │
```

---

## Structure des données

### Serveur

```python
# Lists (Global)
clients = [
    <socket1: Alice>,
    <socket2: Bob>,
    <socket3: Carol>
]

nicknames = [
    "Alice",
    "Bob",
    "Carol"
]

# Tuple
blacklist = (
    '192.168.30.5',  # IP bannies
)

# Semaphore
limiteur = Semaphore(16)  # Max 16 connexions simultanées
```

### Client

```python
# Queue (Thread-safe)
messages_recus = Queue()
# Contient: ["Message 1", "Message 2", ...]

# Dictionnaires
my_nickname = {"nickname": "Alice"}
partage = {"choix": "serveur"}

# Flag
running = True  # Contrôle du thread d'écoute
```

---

## Configuration

### Serveur - Paramètres configurables

```python
# Adresse d'écoute
HOST = '127.0.0.1'  # localhost uniquement
PORT = 9000         # Port d'écoute

# Limites
SEMAPHORE_LIMIT = 16    # Clients max simultanés
SOCKET_BACKLOG = 5      # Connexions en attente

# Timeouts
NICKNAME_TIMEOUT = 30   # Secondes (choisir nickname)
CHOICE_TIMEOUT = 60     # Secondes (choisir mode)
CONTACT_TIMEOUT = 30    # Secondes (choisir destinataire)

# Blacklist
blacklist = (
    '192.168.30.5',     # Ajouter IPs à bannir ici
)
```

### Client - Paramètres configurables

```python
# Connexion
HOST = '127.0.0.1'
PORT = 9000

# Timeouts
GENERAL_TIMEOUT = 5     # Queue.get(timeout=5)
RECEIVE_TIMEOUT = 60    # Attente du serveur

# Buffer
BUFFER_SIZE = 1024      # recv() buffer size
```

---

## Gestion des threads

### Serveur

```
┌─ MAIN THREAD (Serveur)
│  ├─ Bind & Listen
│  ├─ Accept loop
│  └─ Spawn client threads
│
├─ CLIENT THREAD 1 (Alice)
│  ├─ set_nickname()
│  ├─ aiguillage()
│  └─ gerer_* functions
│
├─ CLIENT THREAD 2 (Bob)
│  ├─ set_nickname()
│  ├─ aiguillage()
│  └─ gerer_* functions
│
└─ CLIENT THREAD N (Carol)
   ├─ set_nickname()
   ├─ aiguillage()
   └─ gerer_* functions
```

### Client

```
┌─ MAIN THREAD (UI)
│  ├─ Connexion
│  ├─ Reception messages
│  ├─ Affichage
│  └─ Input utilisateur
│
└─ LISTEN THREAD (Réception)
   ├─ Écoute socket
   ├─ Décode messages
   └─ Put en queue
```

**Synchronisation:** La queue `messages_recus` synchronise les deux threads.

---

## Sécurité

### Implémentée ✅

- **Blacklist d'IP** : Bannir certaines adresses
- **Timeouts** : Éviter les connexions zombies
- **Fermeture propre** : Nettoyage des sockets
- **Thread-safe queue** : Pas de race conditions

### Non implémentée ❌

- **Authentification par mot de passe**
- **Chiffrement SSL/TLS**
- **Validation des messages**
- **Rate limiting** (anti-spam)

---

## Performance

### Limitations actuelles

```
┌─ Nombre de clients ────────── 16 max (Semaphore)
├─ Taille des messages ─────── 1024 bytes
├─ Latence réseau ──────────── ~1-10ms (localhost)
├─ Throughput messages ─────── ~100 msg/sec
└─ Mémoire par client ──────── ~10-50 KB
```

### Bottlenecks

1. **Semaphore(16)** - Limite max clients
2. **recv(1024)** - Messages > 1024 bytes doivent être fragmentés
3. **Global lock** - Accès aux listes clients/nicknames

---

## Diagramme d'états

### État du Client

```
    ┌─────────────────────┐
    │   DÉCONNECTÉ        │
    └──────────┬──────────┘
               │ connect()
               ▼
    ┌─────────────────────┐
    │   CONNECTING        │
    └──────────┬──────────┘
               │ accept()
               ▼
    ┌─────────────────────┐
    │   SET_NICKNAME      │
    └──────────┬──────────┘
               │ nickname OK
               ▼
    ┌─────────────────────┐
    │   READY             │◄─────┐
    └──────────┬──────────┘      │
               │ choose mode      │ exit mode
               ▼                  │
    ┌─────────────────────┐      │
    │   [serveur]         │──────┘
    │   [broadcast]       │
    │   [client]          │
    │   [exit]            │
    └──────────┬──────────┘
               │ exit
               ▼
    ┌─────────────────────┐
    │   CLOSING           │
    └──────────┬──────────┘
               │ close()
               ▼
    ┌─────────────────────┐
    │   DÉCONNECTÉ        │
    └─────────────────────┘
```

---

## Messages de protocole

### Format des messages

```python
# Simple text protocol (no binary)
# UTF-8 encoding

Message format:
<text>\n  # Newline optionnel

Exemples:
"Alice"
"Bonjour tout le monde"
"serveur"
"exit"
```

### Commandes réservées (Serveur)

```
CLIENT -> SERVEUR
├─ "serveur"      → Mode communication serveur
├─ "broadcast"    → Mode broadcast
├─ "client"       → Mode client-to-client
├─ "exit"         → Déconnexion

SERVEUR -> CLIENT
├─ "Bienvenue..." → Greeting
├─ "Entrez..."    → Prompt
├─ "Choisissez..."→ Menu
├─ "Message..."   → Erreur/Info
```

---

## Scalabilité

### Actuellement

```
Clients: 1-16 (Semaphore limit)
Messages/sec: ~100
Mémoire: ~1-5 MB
Uptime: Illimité (théoriquement)
```

### Pour scaler à 100+ clients

1. Augmenter Semaphore(16) → Semaphore(100)
2. Utiliser asyncio au lieu de threading
3. Ajouter une base de données
4. Implémenter un message broker (RabbitMQ)
5. Load balancing (plusieurs serveurs)

```python
# Exemple: Scalabilité limitée

# Actuel (inefficace au-delà de 16)
limiteur = threading.Semaphore(16)

# Amélioré (asyncio)
import asyncio
# Pas de limite stricte, gestion meilleure
```

---

## Déploiement

### Développement (Actuel)

```
Serveur: localhost:9000
Clients: localhost:9000
Network: Local (loopback)
Deployment: Single machine
```

### Production (À faire)

```
Serveur: 0.0.0.0:9000 (tous les IPs)
Clients: server.example.com:9000
Network: Internet
Deployment: 
  ├─ Certificats SSL/TLS
  ├─ Firewall rules
  ├─ Rate limiting
  ├─ Logging central
  ├─ Monitoring
  └─ Backup
```

---

## Diagnostic

### Logs du serveur

```
[CONNEXION] Nouveau client : ('127.0.0.1', 54321)
[NICKNAME] 127.0.0.1 -> Alice
[SERVEUR] Client connecté : ('127.0.0.1', 54321)
[MESSAGE] De ('127.0.0.1', 54321) : texte du message
[BROADCAST] Client connecté : ('127.0.0.1', 54322)
[C2C] De ('127.0.0.1', 54321) : message privé
[LOG] Déconnexion de ('127.0.0.1', 54321)
[ERREUR] Description de l'erreur
```

### Logs du client

```
✓ Connecté au serveur
[INFO] Message reçu du serveur
[MODE SERVEUR] (Tapez 'exit' pour quitter)
[MODE BROADCAST] (Tapez 'exit' pour quitter)
[ERREUR] Description de l'erreur
[INFO] Message envoyé
Vous êtes déconnecté.
```

---

## Checklist d'architecture

- [x] Client-serveur architecture
- [x] Multithreading côté serveur
- [x] Queue thread-safe côté client
- [x] 3 modes de communication
- [x] Gestion des timeouts
- [x] Blacklist d'IP
- [x] Nettoyage des ressources
- [ ] Authentification avancée
- [ ] Chiffrement
- [ ] Base de données
- [ ] Monitoring/metrics

---

**Architecture stable et prête pour l'apprentissage!** 🎓

Pour des modifications, voir `CORRECTIONS_COMPLETES.md`.
