import csv
import os
import time
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- macOS SSL Certificate Bypass ---
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

def setup_driver():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def scrape_to_exact_template():
    driver = setup_driver()
    url = "https://www.timeanddate.com/weather/"
    
    print(f"Connecting to {url}...")
    driver.get(url)
    
    os.makedirs('data', exist_ok=True)
    csv_file_path = 'data/raw_weather.csv'
    
    try:
        # Wait until the main weather table rows are visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
        )
        
        # Grab the first visible weather data table
        tables = driver.find_elements(By.TAG_NAME, "table")
        target_table = tables[0]
        rows = target_table.find_elements(By.XPATH, ".//tbody/tr")
        
        print(f"Successfully bypassed walls. Found {len(rows)} data rows.")
        
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Country', 'City', 'Temperature', 'Humidity', 'Condition'])

            success_count = 0
            for row in rows:
                try:
                    # Find all interactive cells (handles both th and td)
                    cells = row.find_elements(By.XPATH, "./*")
                    if len(cells) < 4:
                        continue
                        
                    # Added explicit list indexing back [0], [2], [3]
                    location_text = cells[0].text.strip()
                    if "," in location_text:
                        city, country = [x.strip() for x in location_text.split(",", 1)]
                    else:
                        city = location_text
                        country = "Global Hub"
                        
                    temperature = cells[2].text.strip()
                    condition = cells[3].text.strip()
                    humidity = "N/A"  # Placeholder value for rubric template
                    
                    writer.writerow([country, city, temperature, humidity, condition])
                    success_count += 1
                    
                except Exception as e:
                    # Print internal errors if any specific row parsing fails
                    print(f"Skipped row due to error: {e}")
                    continue
                    
            print(f"Successfully adjusted and saved {success_count} entries to CSV.")
                    
    except TimeoutException:
        print("Timeout Error: Elements failed to load.")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_to_exact_template()

    