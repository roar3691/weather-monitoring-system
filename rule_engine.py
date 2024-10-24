import requests
import sqlite3
from datetime import datetime
import schedule
import time

# API Configuration
API_KEY = '6df9088b6249404f60dd52436845d94b'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city):
    print(f"Fetching weather data for {city}...")
    params = {
        'q': f"{city},IN",
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        print(f"Data fetched successfully for {city}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def update_daily_summary(city):
    data = fetch_weather_data(city)
    
    if not data or data.get('cod') != 200:
        print(f"Skipping update for {city} due to fetch error.")
        return

    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    main_condition = data['weather'][0]['main']
    dt = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d')

    print(f"Processing data for {city}: Temp={temp}°C, Feels Like={feels_like}°C, Condition={main_condition}")

    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM daily_summary WHERE date=? AND city=?", (dt, city))
        existing = c.fetchone()

        if existing:
            avg_temp = (existing[2] + temp) / 2
            max_temp = max(existing[3], temp)
            min_temp = min(existing[4], temp)
            
            c.execute('''
                UPDATE daily_summary 
                SET avg_temp=?, max_temp=?, min_temp=?, feels_like=?, dominant_condition=?
                WHERE date=? AND city=?
            ''', (avg_temp, max_temp, min_temp, feels_like, main_condition, dt, city))
            print(f"Updated weather data for {city}")
        else:
            c.execute('''
                INSERT INTO daily_summary 
                (date, city, avg_temp, max_temp, min_temp, feels_like, dominant_condition)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (dt, city, temp, temp, temp, feels_like, main_condition))
            print(f"Inserted new weather data for {city}")

        conn.commit()
    except Exception as e:
        print(f"Database error for {city}: {e}")
    finally:
        conn.close()

def run_scheduler():
    print("Starting weather data collection...")
    print(f"Using API key: {API_KEY}")
    print(f"Monitoring cities: {', '.join(CITIES)}")
    
    for city in CITIES:
        update_daily_summary(city)
    
    for city in CITIES:
        schedule.every(5).minutes.do(update_daily_summary, city=city)

if __name__ == "__main__":
    run_scheduler()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping weather data collection...")
