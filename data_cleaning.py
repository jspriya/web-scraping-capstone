import os
import re
import pandas as pd

def process_and_clean_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, 'data', 'raw_weather.csv')
    clean_path = os.path.join(base_dir, 'data', 'cleaned_weather.csv')
    
    if not os.path.exists(raw_path):
        print(f"Pipeline Error: Source data path '{raw_path}' missing. Run scraper.py first.")
        return

    print("\n ===== RUNNING ADVANCED FLEXIBLE POSITION PIPELINE ENGINE =====\n")

    df = pd.read_csv(raw_path)
    print(f"Raw CSV loaded. Processing {len(df)} records...")
    
    clean_rows = []

    for idx, row in df.iterrows():
        # Fall back to numeric indexing to bypass column name mismatches entirely
        # row[0] = Country, row[1] = City, row[2] = Null, row[3] = Raw Temp, row[4] = Condition Context
        country = str(row.iloc[0]).strip()
        city = str(row.iloc[1]).strip()
        
        # 1. Search ALL row columns to extract the temperature integer safely
        temperature_f = None
        for cell_value in row.values:
            cell_str = str(cell_value)
            if 'nbsp' in cell_str or '°' in cell_str:
                match = re.search(r"(-?\d+)", cell_str)
                if match:
                    temperature_f = int(match.group(1))
                    break
                    
        # Secondary fallback if no special characters exist in the row cells
        if temperature_f is None:
            match = re.search(r"(-?\d+)", str(row.iloc[3]))
            if match:
                temperature_f = int(match.group(1))

        # 2. capture the final column value as the target weather condition
        condition = str(row.iloc[-1]).strip()
        if condition == "nan" or not condition:
            condition = "Clear"
            
        # Standardize numeric condition signatures if any are codes
        if condition.isdigit():
            condition = f"Active Status {condition}"

        # 3. Only keep rows with valid temperature parses
        if temperature_f is not None:
            clean_rows.append({
                'country': country,
                'city': city,
                'humidity': 'N/A',
                'condition': condition,
                'temperature_f': temperature_f
            })

        if not clean_rows:
            print("Warning: Standard parsing yielded 0 rows. Executing immediate string extraction fallback...")
            # Direct fallback parser to strip columns by key index positions
            for idx, row in df.iterrows():
                try:
                    raw_t = str(row.iloc[3])
                    t_val = int(raw_t.split('&')[0]) if '&' in raw_t else int(re.search(r"(-?\d+)", raw_t).group(1))
                    clean_rows.append({
                        'country': str(row.iloc[0]),
                        'city': str(row.iloc[1]),
                        'humidity': 'N/A',
                        'condition': f"Status {row.iloc[4]}",
                        'temperature_f': t_val
                    })
                except Exception:
                    continue

    # Reconstruct the cleaned DataFrame
    cleaned_df = pd.DataFrame(clean_rows)
    cleaned_df = cleaned_df.drop_duplicates(subset=['country', 'city'], keep='first')
    
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    cleaned_df.to_csv(clean_path, index=False)
    print(f"🎉 Success! Clean file processed and saved with {len(cleaned_df)} rows at: '{clean_path}'")

if __name__ == "__main__":
    process_and_clean_data()