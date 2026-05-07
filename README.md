# AutoConnect 🇸🇳

Plateforme de vente automobile — Django REST API + React (Vite)

## Stack
- **Backend** : Django 4.2, DRF, JWT (simplejwt + token blacklist), SQLite
- **Frontend** : React 18, Vite, Axios
- **Design** : Dark luxury — `#09090B` bg, `#C9A96E` or, Playfair Display + DM Sans

---

## 🚀 Démarrage rapide

### 1. Backend Django

#### Setup automatique (recommandé)

**Windows :**
```bat
cd backend
setup.bat
```

**Linux / macOS :**
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

Le script crée le venv `env/`, installe les dépendances, applique les migrations et charge les données de démo.

#### Setup manuel

```bash
cd backend

# 1. Créer l'environnement virtuel (dossier env/)
python -m venv env

# 2. Activer
# Windows :
env\Scripts\activate
# Linux/macOS :
source env/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
copy .env.example .env       # Windows
cp .env.example .env         # Linux/macOS
# Puis éditer .env si besoin (SECRET_KEY, DEBUG, etc.)

# 5. Migrations + seed
python manage.py migrate
python manage.py seed_data

# 6. (optionnel) admin Django
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver   # → http://localhost:8000
```

### 2. Frontend React

```bash
cd frontend
npm install
npm run dev    # → http://localhost:3000
```

---

## 🔐 Authentification

L'API utilise **JWT (Bearer)** via `djangorestframework-simplejwt`.
- L'access token expire après **60 min** (configurable via `.env`)
- Le refresh token expire après **7 jours**, rotation automatique
- Le `/api/auth/logout/` blackliste le refresh token côté serveur

### Inscription — champs obligatoires
- email
- mot de passe (min. 6 caractères)
- prénom + nom
- **téléphone** (format sénégalais : `+221 7X XXX XX XX`)
- **numéro CNI** (13 chiffres exactement, unique)
- type de compte : acheteur / vendeur

---

## 📡 API Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/auth/register/` | Créer un compte (avec phone + CNI) |
| POST | `/api/auth/login/` | Connexion → JWT |
| POST | `/api/auth/logout/` | Déconnexion (blacklist du refresh) |
| POST | `/api/token/refresh/` | Rafraîchir l'access token |
| GET | `/api/auth/profile/` | Profil utilisateur |
| PATCH | `/api/auth/profile/update/` | Mettre à jour son profil |
| GET | `/api/cars/` | Liste des voitures (filtrable) |
| GET | `/api/cars/:id/` | Détail d'une voiture |
| GET | `/api/sellers/` | Liste des vendeurs |
| GET/POST | `/api/appointments/` | Rendez-vous |
| PATCH | `/api/appointments/:id/` | Modifier un RDV |
| GET | `/api/favorites/` | Mes favoris |
| POST | `/api/favorites/:id/toggle/` | Ajouter/retirer favori |
| GET | `/api/dashboard/seller/` | Dashboard vendeur |

---

## 🔎 Filtres catalogue (GET /api/cars/)

- `q` — recherche texte (marque, modèle)
- `fuel` — Essence / Diesel / Hybride / Électrique
- `transmission` — Automatique / Manuelle
- `min_price` / `max_price` — fourchette de prix
- `max_mileage` — kilométrage maximum
- `sort` — recent / price-asc / price-desc / mileage

---

## 📁 Structure du projet

```
autoconnect/
├── .gitignore
├── README.md
├── backend/
│   ├── env/                  # ← environnement virtuel Python (créé par setup)
│   ├── .env                  # ← variables d'environnement (NE PAS COMMITTER)
│   ├── .env.example          # ← exemple de config
│   ├── setup.bat             # script setup Windows
│   ├── setup.sh              # script setup Linux/macOS
│   ├── requirements.txt
│   ├── manage.py
│   ├── db.sqlite3
│   ├── autoconnect/          # projet Django (settings dotenv-friendly, urls)
│   ├── users/                # auth + modèle User custom (email, phone, CNI)
│   └── cars/                 # voitures, vendeurs, RDV, favoris
└── frontend/
    ├── package.json
    ├── vite.config.js        # proxy /api → http://localhost:8000
    └── src/
        ├── App.jsx           # navigation + gestion session
        ├── api/index.js      # client axios (intercepteur refresh token)
        └── components/
            ├── Shared.jsx        # Logo, Navbar (avec menu déconnexion), CarCard, tokens
            ├── HomePage.jsx
            ├── Catalogue.jsx
            ├── CarDetail.jsx
            ├── Booking.jsx
            ├── Auth.jsx          # Login / Register (avec téléphone + CNI)
            ├── SellerDashboard.jsx
            ├── BuyerDashboard.jsx
            └── AdminDashboard.jsx
```

---

## 🛠 Corrections récentes

- ✅ Bouton **Se déconnecter** ajouté dans le menu utilisateur de la navbar
- ✅ Endpoint `/api/auth/logout/` qui blackliste le refresh token JWT
- ✅ Intercepteur axios avec **anti-récursion** + refresh token mutualisé entre requêtes concurrentes
- ✅ Synchronisation auto de la déconnexion entre onglets (event `storage`)
- ✅ Validation de la session au démarrage de l'app
- ✅ Champs **téléphone** (format SN) et **CNI** (13 chiffres) obligatoires à l'inscription
- ✅ Configuration via `.env` (SECRET_KEY, DEBUG, etc.) avec `python-dotenv`
- ✅ Environnement virtuel `env/` à l'intérieur de `backend/`
