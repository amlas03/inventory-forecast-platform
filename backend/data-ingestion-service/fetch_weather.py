import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import time
import logging
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_errors.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
CITY = os.getenv('CITY', 'Casablanca')

# Rate limiting
MAX_CALLS_PER_DAY = 100
DELAY_BETWEEN_CALLS = 1  # secondes

class WeatherFetcher:
    def __init__(self):
        self.api_calls_today = 0
        self.last_reset = datetime.now().date()
        
    def get_db_connection(self):
        """Établir une connexion à la base de données"""
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except Exception as e:
            logger.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def check_rate_limit(self):
        """Vérifier et gérer le rate limiting"""
        current_date = datetime.now().date()
        
        # Réinitialiser le compteur si on est un nouveau jour
        if current_date > self.last_reset:
            self.api_calls_today = 0
            self.last_reset = current_date
            logger.info("Compteur d'appels API réinitialisé pour le nouveau jour")
        
        if self.api_calls_today >= MAX_CALLS_PER_DAY:
            logger.warning(f"Limite d'appels API atteinte ({MAX_CALLS_PER_DAY}/jour)")
            return False
        
        return True
    
    def is_data_cached(self, date, city):
        """Vérifier si les données pour cette date et ville existent déjà"""
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            
            cur.execute(
                "SELECT COUNT(*) FROM weather_data WHERE date = %s AND city = %s",
                (date, city)
            )
            count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            return count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du cache: {e}")
            return False
    
    def fetch_current_weather(self, city):
        """Récupérer les données météo actuelles"""
        if not self.check_rate_limit():
            return None
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'en'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            self.api_calls_today += 1
            logger.info(f"Appel API #{self.api_calls_today} effectué pour {city}")
            
            data = response.json()
            
            weather_data = {
                'date': datetime.now().date(),
                'temp': data['main']['temp'],
                'condition': data['weather'][0]['description'],
                'city': city
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la récupération des données météo: {e}")
            return None
        except KeyError as e:
            logger.error(f"Erreur de format de données API: {e}")
            return None
    
    def save_to_database(self, weather_data):
        """Sauvegarder les données dans la base de données"""
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            
            cur.execute(
                """
                INSERT INTO weather_data (date, temp, condition, city)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (date, city) DO UPDATE
                SET temp = EXCLUDED.temp,
                    condition = EXCLUDED.condition,
                    created_at = CURRENT_TIMESTAMP
                """,
                (weather_data['date'], weather_data['temp'], 
                 weather_data['condition'], weather_data['city'])
            )
            
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Données sauvegardées: {weather_data['date']} - {weather_data['city']}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde en base de données: {e}")
            return False
    
    def fetch_historical_data(self, city, days=30):
        """Récupérer les données historiques (simulées avec l'API actuelle)"""
        logger.info(f"Début de la récupération de {days} jours de données pour {city}")
        
        success_count = 0
        cached_count = 0
        error_count = 0
        
        for i in range(days):
            target_date = (datetime.now() - timedelta(days=i)).date()
            
            # Vérifier le cache
            if self.is_data_cached(target_date, city):
                logger.info(f"Données déjà en cache pour {target_date}")
                cached_count += 1
                continue
            
            # Vérifier le rate limit
            if not self.check_rate_limit():
                logger.warning("Rate limit atteint, arrêt de la récupération")
                break
            
            # Récupérer les données
            weather_data = self.fetch_current_weather(city)
            
            if weather_data:
                # Ajuster la date pour simuler l'historique
                weather_data['date'] = target_date
                
                if self.save_to_database(weather_data):
                    success_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
            
            # Délai entre les appels
            time.sleep(DELAY_BETWEEN_CALLS)
        
        logger.info(f"""
        Résumé de la récupération:
        - Succès: {success_count}
        - Déjà en cache: {cached_count}
        - Erreurs: {error_count}
        - Total appels API aujourd'hui: {self.api_calls_today}/{MAX_CALLS_PER_DAY}
        """)

def main():
    logger.info("=== Démarrage du script de récupération météo ===")
    
    # Vérifier que la clé API est configurée
    if not API_KEY:
        logger.error("ERREUR: Clé API non configurée dans le fichier .env")
        return
    
    # Créer l'instance du fetcher
    fetcher = WeatherFetcher()
    
    # Récupérer 30 jours de données
    fetcher.fetch_historical_data(CITY, days=30)
    
    logger.info("=== Script terminé ===")

if __name__ == "__main__":
    main()