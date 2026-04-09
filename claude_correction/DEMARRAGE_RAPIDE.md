# 🚀 DÉMARRAGE RAPIDE

## Prérequis
- Python 3.6+
- Deux terminaux (pour serveur + client)

---

## 5 minutes pour démarrer

### 1️⃣ Terminal 1 - Démarrer le SERVEUR

```bash
python server_corrige.py
```

Vous devriez voir :
```
==================================================
Serveur démarré sur le port 9000...
En attente de connexions...
==================================================
```

✅ **Serveur prêt!**

---

### 2️⃣ Terminal 2 - Démarrer le CLIENT 1

```bash
python client_corrige.py
```

Vous devriez voir :
```
✓ Connecté au serveur
--- Connecté au serveur (Tapez 'exit' pour quitter) ---

Bienvenue sur le serveur ! Entrez votre nickname :
```

Entrez un nickname (ex: `Alice`)

```
> Alice
Bienvenue Alice !
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
```

✅ **Client 1 connecté!**

---

### 3️⃣ Terminal 3 - Démarrer le CLIENT 2 (optionnel)

Répétez l'étape 2 avec un autre nickname (ex: `Bob`)

```bash
python client_corrige.py
```

```
> Bob
Bienvenue Bob !
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
```

✅ **Client 2 connecté!**

---

## 🎮 Test rapide des modes

### Mode 1 : SERVEUR (Parler au serveur)

**Client 1 (Alice) :**
```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> serveur

[MODE SERVEUR] (Tapez 'exit' pour quitter)
Vous : Bonjour le serveur!
Serveur : Message recu par le serveur
Vous : exit
Fin de la conversation.
```

---

### Mode 2 : BROADCAST (Tous les clients)

**Client 1 (Alice) :**
```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> broadcast

[MODE BROADCAST] (Tapez 'exit' pour quitter)
Message à diffuser : Coucou tout le monde!
Message envoyé
Message à diffuser : exit
```

**Client 2 (Bob) reçoit automatiquement :**
```
Coucou tout le monde!
```

---

### Mode 3 : CLIENT-TO-CLIENT (Privé)

**Client 1 (Alice) :**
```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> client

[SERVEUR] Entrez le nickname du client à contacter :
Nom du destinataire : Bob
[SERVEUR] (En attente...)
Message : Salut Bob!
```

**Client 2 (Bob) reçoit :**
```
Salut Bob!
```

---

### Mode 4 : EXIT (Déconnexion)

```
Choisissez : 'serveur', 'broadcast', 'client', ou 'exit' :
> exit

Déconnexion demandée.
Déconnexion du serveur...
Vous êtes déconnecté.
```

---

## ✅ Checklist de vérification

- [ ] Serveur lancé et en écoute sur port 9000
- [ ] Client 1 connecté avec nickname unique
- [ ] Client 2 connecté avec nickname unique
- [ ] Mode serveur fonctionne
- [ ] Mode broadcast fonctionne
- [ ] Mode client-to-client fonctionne
- [ ] Les deux clients peuvent communiquer
- [ ] Déconnexion propre (exit)

---

## 🆘 Aide rapide

### Erreur : "Connection refused"
```bash
❌ Serveur pas lancé?
✅ Solution: Lancez server_corrige.py d'abord
```

### Erreur : "Address already in use"
```bash
❌ Port 9000 déjà utilisé?
✅ Solution Linux/Mac:
   lsof -ti :9000 | xargs kill -9

✅ Solution Windows:
   netstat -ano | findstr :9000
   taskkill /PID <PID> /F
```

### Le programme freeze
```bash
❌ Bloqué lors du timeout?
✅ Solution: Attendez max 60 secondes
✅ Ou appuyez sur Ctrl+C pour fermer
```

### Message reçu pas visible
```bash
❌ En mode serveur?
✅ C'est normal, attendez votre tour

❌ En mode broadcast?
✅ L'expéditeur ne voit PAS son propre message

❌ En mode client-client?
✅ Vérifiez que le destinataire existe
```

---

## 📊 Vue du serveur

Ce que vous verrez sur le **Terminal 1 (Serveur)** :

```
[CONNEXION] Nouveau client : ('127.0.0.1', 54321)
[NICKNAME] 127.0.0.1 -> Alice
[SERVEUR] Client connecté : ('127.0.0.1', 54321)
[MESSAGE] De ('127.0.0.1', 54321) : Bonjour le serveur
[LOG] Déconnexion de ('127.0.0.1', 54321)
```

---

## 🎯 Cas d'usage avancés

### Scénario 1 : Chat de groupe

1. Lancez 1 serveur
2. Connectez 5+ clients
3. Chaque client choisit **broadcast**
4. Tous les messages sont diffusés à tous

### Scénario 2 : Support technique

1. Client = Utilisateur (Alice)
2. Serveur = Support (mode serveur)
3. Alice parle au serveur
4. Serveur répond

### Scénario 3 : Messages privés

1. Alice et Bob se connectent
2. Alice choisit `client` → contacter Bob
3. Communication privée entre Alice et Bob
4. Carol ne voit rien

---

## 💡 Conseils

✅ **Nicknames uniques** - Deux clients ne peuvent pas avoir le même
✅ **Tapez proprement** - Les commandes sont sensibles à la casse (`serveur`, pas `SERVEUR`)
✅ **Utilisez exit** - Quittez proprement avec `exit` plutôt que Ctrl+C
✅ **Un mode à la fois** - Choisissez UNE option, puis un autre après
✅ **Attendez la réponse** - Laissez le serveur répondre avant de continuer

---

## 🔍 Structure de fichiers

```
.
├── server_corrige.py        # Serveur (lancez en 1er)
├── client_corrige.py        # Client (lancez après)
├── README.md                # Documentation complète
├── DEMARRAGE_RAPIDE.md      # Ce fichier
└── CORRECTIONS_COMPLETES.md # Historique des bugs
```

---

## ⏱️ Durées importantes

| Action | Timeout | Effet |
|--------|---------|-------|
| Choisir nickname | 30s | Déconnexion auto |
| Choisir mode | 60s | Déconnexion auto |
| Choisir destinataire | 30s | Déconnexion auto |
| Réponse serveur | 5s | Affiche timeout |
| Connection | 10s | Impossible se connecter |

---

## 🎓 Résumé rapide

| Mode | Usage | Raccourci |
|------|-------|----------|
| `serveur` | Parler au serveur | `ser` ou `s` |
| `broadcast` | Message à tous | `bro` ou `b` |
| `client` | Message privé | `cli` ou `c` |
| `exit` | Quitter | `ex` ou `e` |

---

## ✨ Prochaines étapes

Après ce test rapide:

1. 📖 Lisez le `README.md` complet
2. 🔧 Explorez le code source
3. 🐛 Reportez les bugs trouvés
4. ⭐ Améliorez les fonctionnalités

---

## 🆘 En cas de souci

### Problème 1: Rien ne s'affiche
```
➜ Appuyez sur Enter
➜ Vérifiez votre typage
➜ Relancez client et serveur
```

### Problème 2: Serveur ne se lance pas
```
➜ Vérifiez Python: python --version
➜ Vérifiez port 9000 libre
➜ Vérifiez fichier exists: server_corrige.py
```

### Problème 3: Client ne se connecte pas
```
➜ Serveur lancé? (Terminal 1)
➜ Port correct? (9000)
➜ Firewall bloque?
```

---

## 🎉 Bravo!

Si vous avez réussi tous les tests, votre chat TCP fonctionne! 🚀

Pour plus de détails, consultez `README.md`

**Amusez-vous bien!** 💬
