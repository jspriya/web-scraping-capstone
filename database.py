import os
import sqlite3
import pandas as pd

def database():
    # Set explicit absolute folder paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_csv_path = os.path.join(base_dir, 'data', 'cleaned_weather.csv')
    db_path = os.path.join(base_dir, 'data', 'weather_data.db')
    
    print("Running simplified database pipeline...")
    
    # 1. Open transactional database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Clear old matching schemas to allow fresh, clean testing loops
    cursor.execute("DROP TABLE IF EXISTS global_weather;")
    
    # 3. Stream data frame columns straight into SQLite
    df = pd.read_csv(cleaned_csv_path)
    df.columns = [col.lower() for col in df.columns]  # Enforce standardized lower-case labels
    df.to_sql('global_weather', conn, index=False, if_exists='append')
    
    # 4. Execute Native SQL Math Transformations to verify system integrity
    cursor.execute("SELECT COUNT(*), AVG(temperature_f) FROM global_weather;")
    total_count, avg_temp = cursor.fetchone()
    
    print("\n--- SQLite Database Live Summary ---")
    print(f"Total Rows Ingested: {total_count}")
    print(f"Global Average Temperature: {round(avg_temp, 1)}°F")
    print(f"Database successfully finalized at: '{db_path}'\n")
    
    conn.close()

if __name__ == "__main__":
    database()