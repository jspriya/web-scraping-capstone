import os
import sqlite3

def run_queries():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'weather_data.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n===== WEATHER DATABASE QUERIES =====\n")

    # Total records
    cursor.execute("SELECT COUNT(*) FROM global_weather")
    total = cursor.fetchone()[0]
    print(f"Total Weather Records: {total}")

    # Average temperature
    cursor.execute("SELECT AVG(temperature_f) FROM global_weather")
    avg_temp = cursor.fetchone()[0]
    print(f"Average Temperature: {avg_temp:.1f}°F")

    # Top 5 hottest cities
    print("\nTop 5 Hottest Cities:")
    cursor.execute("""
        SELECT city, country, temperature_f
        FROM global_weather
        ORDER BY temperature_f DESC
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    # Top 5 coldest cities
    print("\nTop 5 Coldest Cities:")
    cursor.execute("""
        SELECT city, country, temperature_f
        FROM global_weather
        ORDER BY temperature_f ASC
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    # Weather condition distribution
    print("\nWeather Conditions:")
    cursor.execute("""
        SELECT condition, COUNT(*)
        FROM global_weather
        GROUP BY condition
        ORDER BY COUNT(*) DESC
    """)

    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    run_queries()

