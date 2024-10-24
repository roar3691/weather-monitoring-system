import sqlite3

def setup_database():
    print("Setting up the database...")
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Create table to store daily summaries with city column
    c.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        date TEXT,
        city TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        feels_like REAL,
        dominant_condition TEXT,
        PRIMARY KEY (date, city)
    )
    ''')

    conn.commit()
    print("Database setup complete.")
    
    # Remove existing data for testing
    try:
        c.execute("DELETE FROM daily_summary")
        print("Existing data removed from the daily_summary table.")
    except Exception as e:
        print(f"Error removing data: {e}")

    # Insert test data including feels_like
    test_data = [
        ('2024-10-23', 'Delhi', 25.0, 30.0, 20.0, 26.0, 'Clear'),
        ('2024-10-23', 'Mumbai', 27.0, 32.0, 22.0, 28.0, 'Haze'),
        ('2024-10-23', 'Chennai', 29.0, 34.0, 25.0, 30.0, 'Sunny'),
        ('2024-10-23', 'Bangalore', 24.0, 29.0, 21.0, 25.0, 'Rain'),
        ('2024-10-23', 'Kolkata', 26.0, 31.0, 23.0, 27.0, 'Thunderstorms'),
        ('2024-10-23', 'Hyderabad', 28.0, 33.0, 24.0, 29.0, 'Clear')
    ]

    try:
        c.executemany("INSERT INTO daily_summary (date, city, avg_temp, max_temp, min_temp, feels_like, dominant_condition) VALUES (?, ?, ?, ?, ?, ?, ?)", test_data)
        conn.commit()
        print("Test data added successfully with feels_like temperatures.")
    except Exception as e:
        print(f"Error inserting test data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
