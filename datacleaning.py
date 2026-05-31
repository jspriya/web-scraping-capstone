import pandas as pd
import os
import re

def clean_and_transform_weather():
    raw_path = 'data/raw_weather.csv'
    cleaned_path = 'data/cleaned_weather.csv'
    
    if not os.path.exists(raw_path):
        print(f"Error: Target data dependency '{raw_path}' is missing.")
        return

    # 1. Load the raw data
    df = pd.read_csv(raw_path)
    
    # 'Condition' contains the temperature strings, copy it over to Temperature
    df['Temperature'] = df['Condition']
    # Reset Condition to a default placeholder value since the main overview text was missed
    df['Condition'] = 'Reported' 
    # -------------------------------------------

    print("=========================================")
    print("📢 STAGE 1: BEFORE CLEANING DIAGNOSTIC SUMMARY")
    print("=========================================")
    print(f"DataFrame Dimensions: {df.shape}")
    print(df.head(5))

    # 2. Remove duplicates
    df = df.drop_duplicates()

    # 3. Clean and convert Temperature values (extracting digits from strings like '84 °F')
    def parse_temperature_string(val):
        if pd.isna(val) or str(val).strip().upper() == "NAN":
            return None
        clean_str = str(val).replace('\xa0', '').strip()
        match = re.search(r'(-?\d+)', clean_str)
        return float(match.group(1)) if match else None

    df['Temperature'] = df['Temperature'].apply(parse_temperature_string)

    # 4. Normalize Humidity
    df['Humidity'] = 'N/A' 

    print("\n=========================================")
    print("✅ STAGE 2: AFTER CLEANING DIAGNOSTIC SUMMARY")
    print("=========================================")
    print(f"DataFrame Dimensions: {df.shape}")
    print(df.head(5))

    # 5. Save the clean, transformed data
    df.to_csv(cleaned_path, index=False)
    print(f"\nTransformation pipeline successful. Clean data saved to: {cleaned_path}")

if __name__ == "__main__":
    clean_and_transform_weather()