# 📋 RÉSUMÉ COMPLET DES CORRECTIONS

## 🔴 SERVEUR - CORRECTIONS

### ❌ Erreur 1: `set_nickname()` ligne 85
**AVANT:**
```python
client_socket.send("Bienvenue sur le serveur !entrez votre nickname :").encode()
```
**PROBLÈME:** `.send()` retourne un nombre, pas une string. Tu ne peux pas faire `.encode()` sur un int.

**APRÈS:**
```python
client_socket.send("Bienvenue sur le serveur ! Entrez votre nickname :".encode())
```

---

### ❌ Erreur 2: `demander_choix()` ligne 130
**AVANT:**
```python
client.send("choix de communication").encode()
```

**APRÈS:**
```python
msg = "Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :"
client.send(msg.encode())
```

---

### ❌ Erreur 3: `demander_choix()` ligne 145
**AVANT:**
```python
client.send("pas de choix a ete enregistré").encode()
```

**APRÈS:**
```python
client.send("Pas de choix enregistré.".encode())
```

---

### ❌ Erreur 4: `demander_choix()` ligne 155
**AVANT:**
```python
client.close  # ← Pas les parenthèses!
```

**APRÈS:**
```python
client.close()
```

---

### ❌ Erreur 5: `broadcast()` ligne 26-35
**AVANT:**
```python
def broadcast(message, _client):
    try:
        while True:  # ← BOUCLE INFINIE!
            for client in clients:
                if client != _client:
                    client.send(message.encode())
```

**PROBLÈME:** Boucle infinie qui envoie le MÊME message continuellement.

**APRÈS:**
```python
def broadcast(message, _client):
    try:
        for client in clients:  # ← Pas de while True
            if client != _client:
                client.send(message.encode())
```

---

### ❌ Erreur 6: `blacklist` ligne 6
**AVANT:**
```python
blacklist = ('192.168.300.5', 9999)  # ← IP invalide! 300 > 255
```

**APRÈS:**
```python
blacklist = ('192.168.30.5',)  # ← IP valide
```

---

### ❌ Erreur 7: `choisir_nickname_a_contacter()` ligne 115
**AVANT:**
```python
client_socket.send("l'utilisateur {} n'est pas en ligne.".format(nickname_a_contacter)).encode()
# ← .encode() sur résultat de .send()
```

**APRÈS:**
```python
msg = f"L'utilisateur {nickname_a_contacter} n'est pas en ligne."
client_socket.send(msg.encode())
```

---

### ❌ Erreur 8: Gestion des exceptions
**AVANT:** Pas de gestion d'exceptions en detail

**APRÈS:** Ajout de try/except/finally partout avec nettoyage correct
```python
finally:
    if client in clients:
        clients.remove(client)
    mon_nickname = get_nickname(client)
    if mon_nickname != "Unknown" and mon_nickname in nicknames:
        nicknames.remove(mon_nickname)
    client.close()
```

---

## 🔴 CLIENT - CORRECTIONS

### ❌ Erreur 1: `set_nickname()` ligne 32-33
**AVANT:**
```python
def set_nickname(client):
    nickname = input("donner votre nickname")
    client.send(nickname).encode()  # ← FAUX!
```

**PROBLÈME:** `send()` retourne un int. Tu ne peux pas faire `.encode()` sur un int.

**APRÈS:**
```python
def set_nickname(client):
    nickname = input("Entrez votre nickname : ")
    client.send(nickname.encode())  # ✓ encode() AVANT send()
```

---

### ❌ Erreur 2: `demande_saisie()` ligne 37-44
**AVANT:**
```python
def demande_saisie(partage):
    try:
        while partage["choix"] == None:  # ← Boucle inutile
            partage["choix"] = input("Entrez votre commande : ")
        return partage  # ← Retourne le DICT!
```

**PROBLÈME:**
1. Retourne un dictionnaire au lieu d'une string
2. Ensuite `dict.lower()` → AttributeError

**APRÈS:**
```python
def demande_saisie():
    return input("Entrez votre commande (serveur/broadcast/client/exit) : ")
```

---

### ❌ Erreur 3: `comm_client_client()` ligne 58
**AVANT:**
```python
instruction = messages_recus.get()  # ← BLOQUANT SANS TIMEOUT!
```

**PROBLÈME:** `.get()` bloque indéfiniment si la queue est vide → FREEZE complet.

**APRÈS:**
```python
try:
    instruction = messages_recus.get(timeout=5)  # ✓ Timeout de 5 secondes
    print(f"[SERVEUR] {instruction}")
except queue.Empty:
    print("[ERREUR] Pas de réponse du serveur (timeout)")
    return
```

---

### ❌ Erreur 4: `choix()` ligne 46-47
**AVANT:**
```python
partage["choix"] = None
partage["choix"] = demande_saisie(partage)  # ← Reçoit un dict

commande = partage["choix"].lower().strip()  # ← dict.lower() → ERROR!
```

**APRÈS:**
```python
commande = demande_saisie().lower().strip()  # ✓ Directement une string
```

---

### ❌ Erreur 5: `broadcast` et `serveur` modes - ligne 74, 82
**AVANT:**
```python
elif commande == "broadcast":
    client.send(commande.encode())
    while True:
        msg = input("Message à diffuser : ")
        client.send(msg.encode())
        print(f"Serveur : {client.recv(1024).decode()}")  # ← RACE CONDITION!
```

**PROBLÈME:**
1. `client.recv()` bloque directement sur le socket
2. Mais `ecouter_serveur` thread lit AUSSI sur le même socket
3. **RACE CONDITION** → les deux threads se battent pour lire
4. Freeze imprévisible

**APRÈS:**
```python
elif commande == "broadcast":
    client.send("broadcast".encode())
    print("\n[MODE BROADCAST] (Tapez 'exit' pour quitter)")
    while True:
        msg = input("Message à diffuser : ")
        if msg.lower() == "exit":
            break
        client.send(msg.encode())
        # ✓ Utilise la queue au lieu de recv()
        try:
            reponse = messages_recus.get(timeout=5)
            print(f"Serveur : {reponse}")
        except queue.Empty:
            print("[INFO] Message envoyé")
```

---

### ❌ Erreur 6: `main()` ligne 115-120
**AVANT:**
```python
while True:
    instruction = messages_recus.get()  # ← BLOQUANT SANS TIMEOUT!
    print(instruction)
    if instruction.lower()=="Bienvenue sur le serveur !entrez votre nickname :":
        # ← Comparaison EXACTE et fragile
```

**PROBLÈME:**
1. `.get()` sans timeout → FREEZE si la queue est vide
2. Comparaison exacte de strings → fragile

**APRÈS:**
```python
while running:
    try:
        instruction = messages_recus.get(timeout=5)  # ✓ Timeout
        print(instruction)
        
        # ✓ Comparaison flexible avec "in"
        if "bienvenue" in instruction.lower() and "nickname" in instruction.lower():
            set_nickname(client)
            
        elif "choix" in instruction.lower() or "choisissez" in instruction.lower():
            choix(client)
        else:
            print(f"[INFO] {instruction}")
            
    except queue.Empty:
        continue  # ✓ Continue sans freezer
```

---

## 📊 TABLE COMPLÈTE DES CORRECTIONS

| # | Fichier | Ligne | Erreur | Type | Fix |
|---|---------|-------|--------|------|-----|
| 1 | SERVER | 85 | `.send(...).encode()` | Syntaxe | `.send(...encode())` |
| 2 | SERVER | 130 | `.send(...).encode()` | Syntaxe | `.send(...encode())` |
| 3 | SERVER | 26-35 | Boucle infinie dans broadcast | Logique | Enlever `while True` |
| 4 | SERVER | 6 | IP invalide (300 > 255) | Donnée | `192.168.30.5` |
| 5 | SERVER | 155 | `client.close` sans () | Syntaxe | `client.close()` |
| 6 | SERVER | 115 | `.send(...).encode()` | Syntaxe | `.send(...encode())` |
| 7 | CLIENT | 33 | `send().encode()` | Syntaxe | `send(encode())` |
| 8 | CLIENT | 37-44 | Retourne dict au lieu de string | Logique | Retourner juste input() |
| 9 | CLIENT | 47 | dict.lower() sur dict | Runtime | Utiliser string directement |
| 10 | CLIENT | 58 | `.get()` sans timeout | Race Condition | `get(timeout=5)` |
| 11 | CLIENT | 74, 82 | `recv()` directe (race condition) | Race Condition | Utiliser `messages_recus.get()` |
| 12 | CLIENT | 115 | `.get()` sans timeout | Race Condition | `get(timeout=5)` |
| 13 | CLIENT | 116 | Comparaison exacte fragile | Logique | Utiliser `"in"` |

---

## ✅ FICHIERS CORRIGÉS

**Serveur:** `server_corrige.py`
**Client:** `client_corrige.py`

Les fichiers sont prêts à l'emploi! 🚀
