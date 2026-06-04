# 🔐 projet-api-mdp

Collection de trois scripts Python indépendants couvrant la **génération de mots de passe sécurisés**, la **simulation de pare-feu réseau**, et la **géolocalisation de numéros de téléphone** avec visualisation cartographique interactive.

---

## 📁 Structure du projet

```
projet-api-mdp/
└── API-mdp/
    ├── generer mot de passe.py     # Générateur de mots de passe configurable
    ├── generer ip + action.py      # Simulateur de règles pare-feu
    └── map succés.py               # Géolocalisation de numéros + carte Folium
```

---

## 📜 Scripts

---

### 1. `generer mot de passe.py` — Générateur de mots de passe sécurisé

#### Description

Ce script génère un mot de passe aléatoire en respectant des critères de sécurité définis interactivement par l'utilisateur : longueur minimale, présence de chiffres, et présence de caractères spéciaux. Il garantit que le mot de passe généré satisfait **obligatoirement** tous les critères choisis avant de le retourner.

#### Fonctionnement détaillé

1. **Construction du pool de caractères** : Le script commence avec les lettres de l'alphabet (minuscules + majuscules via `string.ascii_letters`). Si l'utilisateur veut des chiffres, `string.digits` est ajouté au pool. Idem pour les caractères spéciaux avec `string.punctuation`.

2. **Boucle de génération avec garantie** : Le mot de passe est construit caractère par caractère en tirant aléatoirement dans le pool. Deux drapeaux booléens (`has_numbers`, `has_special`) tracent si au moins un chiffre et/ou un caractère spécial ont été inclus. La boucle **continue tant que** la longueur minimale n'est pas atteinte **ET** que tous les critères demandés ne sont pas satisfaits, ce qui évite qu'un mot de passe de longueur exactement minimale soit retourné sans contenir les types de caractères requis.

3. **Interaction en console** : L'utilisateur saisit la longueur minimale et répond `y`/`n` pour activer les chiffres et les caractères spéciaux.

#### Dépendances

| Module | Usage | Stdlib |
|--------|-------|--------|
| `random` | Sélection aléatoire de caractères | ✅ |
| `string` | Jeux de caractères prédéfinis | ✅ |

Aucune installation nécessaire.

#### Utilisation

```bash
python "generer mot de passe.py"
```

**Exemple d'exécution :**
```
enter la longueur minimum : 12
est ce que vous voulez avoir des nombres (y/n) : y
est ce que vous voulez avoir des spécials (y/n) : y
le mot de passe généré est =  rT#4kP!mQ2xZ
```

#### Points clés du code

```python
def generer_mot_de_passe(min_length, numbers=True, special_characters=True):
    # Boucle garantissant que tous les critères sont satisfaits
    while not meets_criteriar or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char
        ...
```

> **Remarque** : La logique `meets_criteriar` est réinitialisée à `True` à chaque itération puis vérifiée par rapport aux flags `has_numbers` et `has_special`. Cela assure que le mot de passe n'est retourné que lorsqu'il est complet et conforme.

---

### 2. `generer ip + action.py` — Simulateur de règles pare-feu

#### Description

Ce script simule le comportement d'un **pare-feu réseau basique** : il génère aléatoirement des adresses IP dans le sous-réseau `192.168.1.0/24` (plage `192.168.1.0` → `192.168.1.20`), les confronte à un ensemble de règles de blocage prédéfinies, et affiche l'action décidée (`block` ou `allow`) ainsi qu'un numéro de transaction aléatoire.

#### Fonctionnement détaillé

1. **`generate_random_ip()`** : Génère une IP dans `192.168.1.{0..20}` via `random.randint`. La plage restreinte (0 à 20) augmente la fréquence de collision avec les IPs bloquées, rendant la simulation plus démonstrative.

2. **`check_firewall_rules(ip, rules)`** : Parcourt un dictionnaire `firewall_rules` où chaque clé est une IP bloquée et la valeur est `"block"`. Si l'IP générée correspond à une règle, cette action est retournée. Sinon, la politique par défaut **permissive** (`"allow"`) s'applique — ce qui reflète une logique de liste noire (*blacklist*).

3. **Boucle principale** : 12 itérations simulant 12 paquets réseau. Pour chaque paquet, l'IP, l'action et un identifiant aléatoire (0–9999) sont affichés — ce dernier pouvant représenter un numéro de port ou un ID de transaction.

#### Adresses IP bloquées (règles prédéfinies)

| IP | Action |
|----|--------|
| 192.168.1.1 | block |
| 192.168.1.4 | block |
| 192.168.1.9 | block |
| 192.168.1.13 | block |
| 192.168.1.16 | block |
| 192.168.1.19 | block |

#### Dépendances

| Module | Usage | Stdlib |
|--------|-------|--------|
| `random` | Génération d'IPs et d'identifiants | ✅ |

Aucune installation nécessaire.

#### Utilisation

```bash
python "generer ip + action.py"
```

**Exemple de sortie :**
```
IP: 192.168.1.7,  Action: allow,  Random: 3821
IP: 192.168.1.1,  Action: block,  Random: 9104
IP: 192.168.1.9,  Action: block,  Random: 512
IP: 192.168.1.14, Action: allow,  Random: 7733
...
```

#### Points clés du code

```python
def check_firewall_rules(ip, rules):
    for rule_ip, action in rules.items():
        if ip == rule_ip:
            return action
    return "allow"  # Politique par défaut : permissive (blacklist)
```

> **Extension possible** : Pour une politique **restrictive** (whitelist), il suffirait de changer la valeur de retour par défaut à `"block"` et de ne lister que les IPs autorisées.

---

### 3. `map succés.py` — Géolocalisation de numéro de téléphone + carte interactive

#### Description

Script le plus avancé du projet : il prend un numéro de téléphone en entrée, identifie le **pays** et l'**opérateur téléphonique** associés via la librairie `phonenumbers`, géocode le pays via l'API **OpenCage**, puis génère une **carte interactive Folium** (fichier HTML) pointant vers la localisation géographique correspondante. La carte est automatiquement ouverte dans le navigateur à la fin de l'exécution.

> 🎥 **Démo vidéo** : [Voir sur Google Drive](https://drive.google.com/file/d/1yoT8yIcStuVL9lTN5Ns6GPrhdtcr6emM/view?usp=sharing)

#### Fonctionnement détaillé

1. **Parsing du numéro** (`phonenumbers.parse`) : Le numéro est parsé au format E.164 (ex. `+212704845996`). Cette étape valide la structure du numéro et extrait le code pays.

2. **Résolution du pays** :
   - En priorité, `phonenumbers.geocoder.description_for_number()` tente de retourner une description géographique en anglais.
   - En fallback, un dictionnaire `prefix_to_country` mappe les préfixes connus (`+212` → Maroc, `+33` → France, `+1` → États-Unis) si le geocoder ne retourne rien.

3. **Identification de l'opérateur** : `phonenumbers.carrier.name_for_number()` retourne le nom de l'opérateur (ex. `Maroc Telecom`, `Orange`, etc.) quand disponible.

4. **Geocodage de la localisation** : L'API REST **OpenCage Geocoder** reçoit le nom du pays/région et retourne les coordonnées GPS (latitude, longitude). Une clé API est requise (incluse en dur dans le script — à externaliser dans un `.env` en production).

5. **Génération de la carte** : `folium.Map` crée une carte centrée sur les coordonnées avec un zoom adapté (`zoom_start=9`). Un marqueur avec popup est ajouté. La carte est sauvegardée en `mylocation.html`.

6. **Ouverture automatique** : `webbrowser.open()` ouvre le fichier HTML dans le navigateur par défaut.

#### Dépendances

| Module | Usage | Installation |
|--------|-------|-------------|
| `phonenumbers` | Parsing, geocoder, carrier | `pip install phonenumbers` |
| `opencage` | API de geocodage (pays → GPS) | `pip install opencage` |
| `folium` | Génération de carte Leaflet.js | `pip install folium` |
| `webbrowser` | Ouverture du navigateur | ✅ Stdlib |

#### Installation

```bash
pip install phonenumbers opencage folium
```

#### Configuration de la clé API OpenCage

Le script contient une clé API OpenCage directement dans le code :

```python
key = '11136cecc87b41529d958c1f0aa4ec45'
```

> ⚠️ **Bonne pratique** : En production ou sur un dépôt public, cette clé doit être externalisée dans un fichier `.env` et chargée via `python-dotenv` :
> ```python
> from dotenv import load_dotenv
> import os
> load_dotenv()
> key = os.getenv("OPENCAGE_API_KEY")
> ```

Pour obtenir une clé gratuite : [opencagedata.com](https://opencagedata.com/)

#### Utilisation

```bash
python "map succés.py"
```

Le script utilise le numéro `+212704845996` (Maroc) codé en dur. Pour tester d'autres numéros, modifier la variable `number` en ligne 15 :

```python
# Exemples commentés dans le script :
# number = "+971525430693"   # EAU
# number = "+33635375954"    # France
number = "+212704845996"     # Maroc (actif)
```

**Sortie console :**
```
Numéro importé : +212704845996
Le nom du pays est : Morocco
Opérateur téléphonique : Maroc Telecom
Latitude: 31.7917 Longitude: -7.0926
Carte enregistrée sous 'mylocation.html'
```

La carte `mylocation.html` s'ouvre ensuite automatiquement dans le navigateur.

#### Points clés du code

```python
# Fallback manuel si le geocoder phonenumbers échoue
if location_en.strip():
    location = location_en
else:
    for prefix, country in prefix_to_country.items():
        if number.startswith(prefix):
            location = country
            break
```

---

## 🚀 Installation globale

```bash
git clone https://github.com/penelopeeckhar/projet-api-mdp.git
cd projet-api-mdp/API-mdp

# Dépendances pour map succés.py uniquement
pip install phonenumbers opencage folium

# Les deux autres scripts n'ont aucune dépendance externe
```

---

## 🔧 Améliorations suggérées

| Script | Amélioration |
|--------|-------------|
| `generer mot de passe.py` | Ajouter une option de longueur **maximale** ; afficher un score de robustesse |
| `generer ip + action.py` | Supporter des plages CIDR (ex. `192.168.1.0/28`) ; logger les événements dans un fichier |
| `map succés.py` | Prendre le numéro en argument CLI (`argparse`) ; externaliser la clé API dans `.env` ; supporter plusieurs numéros simultanément |

---

## 👤 Auteur

**Abir Majdi** — [github.com/penelopeeckhar](https://github.com/penelopeeckhar)
