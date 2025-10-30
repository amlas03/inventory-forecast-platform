# 🌤️ Weather Data Fetching Setup

Système de récupération automatique de données météo avec OpenWeatherMap API et PostgreSQL. Inclut rate limiting, caching intelligent et logging des erreurs.

---

## 📋 Prérequis

- Python 3.8+
- PostgreSQL 12+
- Compte OpenWeatherMap (gratuit)

---

## ⚡ Installation Rapide

### 1. Clone et Setup

```bash
# Cloner le repo
git clone https://github.com/ton-username/ton-repo.git
cd ton-repo

# Créer environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Installer dépendances
pip install requests psycopg2-binary python-dotenv
```

### 2. Configuration OpenWeatherMap

1. Créer un compte sur [openweathermap.org](https://openweathermap.org/api)
2. Aller dans **My API keys**
3. Copier votre clé API (attend 10-15 min pour activation)

### 3. Configuration PostgreSQL

**Ouvrir psql ou pgAdmin et exécuter :**

```sql
-- Créer la base de données
CREATE DATABASE weather_db;

-- Se connecter
\c weather_db

-- Créer la table
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    temp DECIMAL(5, 2) NOT NULL,
    condition VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, city)
);
```

### 4. Configuration Environnement

Créer un fichier `.env` à la racine du projet :

```env
# API OpenWeatherMap
OPENWEATHER_API_KEY=ta_cle_api_ici

# PostgreSQL
DB_HOST=localhost
DB_PORT=5433
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=ton_mot_de_passe

# Configuration
CITY=Casablanca
```

⚠️ **Important :** Ajouter `.env` au `.gitignore`

```bash
echo ".env" >> .gitignore
```

---

## 🚀 Utilisation

### Lancer le script

```bash
python fetch_weather.py
```

**Première exécution :** Récupère 30 jours de données (~30 secondes, 30 appels API)

**Exécutions suivantes :** Utilise le cache, 0 appel API si données déjà présentes

### Vérifier les données

**Via psql :**
```sql
\c weather_db
SELECT * FROM weather_data ORDER BY date DESC LIMIT 10;
```

**Via pgAdmin :**
- Ouvrir Query Tool sur `weather_db`
- Exécuter : `SELECT * FROM weather_data ORDER BY date DESC;`

### Consulter les logs

```bash
cat weather_errors.log    # Mac/Linux
type weather_errors.log   # Windows
```

---

## 📊 Fonctionnalités

- ✅ **Rate Limiting** : Respecte la limite de 100 appels/jour
- ✅ **Caching intelligent** : Ne refetch pas les données existantes
- ✅ **Logging complet** : Toutes les opérations dans `weather_errors.log`
- ✅ **Gestion d'erreurs** : Continue en cas d'échec ponctuel
- ✅ **Reset automatique** : Compteur remis à 0 chaque jour

---

## 🆘 Troubleshooting

### `ModuleNotFoundError: No module named 'requests'`
```bash
pip install requests psycopg2-binary python-dotenv
```

### `could not connect to server`
Vérifier que PostgreSQL est démarré :
```bash
# Windows
net start postgresql-x64-15

# Mac
brew services start postgresql@15

# Linux
sudo systemctl start postgresql
```

### `401 Client Error: Unauthorized`
- Attendre 10-15 min après création de la clé API
- Vérifier que la clé dans `.env` est correcte
- Pas d'espaces avant/après la clé

### `Rate limit atteint`
Limite de 100 appels/jour atteinte. Attendre demain ou utiliser les données en cache.

### Script s'exécute mais aucune donnée
Vérifier les logs :
```bash
cat weather_errors.log
```

---

## 📝 Structure du Projet

```
weather_project/
├── fetch_weather.py      # Script principal
├── .env                  # Configuration (ne pas commit!)
├── weather_errors.log    # Logs générés automatiquement
├── .gitignore           # Exclure .env
└── README.md            # Ce fichier
```

---

## 🔒 Sécurité

- ❌ **Ne jamais commit le fichier `.env`**
- ✅ Toujours ajouter `.env` au `.gitignore`
- ✅ Utiliser des mots de passe forts pour PostgreSQL
- ✅ Ne pas partager votre clé API

---

## 📈 Limitations

**Free Tier OpenWeatherMap :**
- 100 appels API / jour
- Données météo actuelles uniquement (pas d'historique réel)
- Le script simule l'historique en sauvegardant les données actuelles avec différentes dates

**Pour des données historiques réelles :**
- Abonnement payant OpenWeatherMap requis
- Ou utiliser une API alternative

---

## 🤝 Support

Pour toute question ou problème :
1. Consulter la section Troubleshooting
2. Vérifier les logs (`weather_errors.log`)
3. Ouvrir une issue sur GitHub

---

## 📄 License

MIT License - Libre d'utilisation

---

**Prêt à commencer ? 🚀**

```bash
python fetch_weather.py
```