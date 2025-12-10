import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import os
import re

def scrape_wikipedia_population():
    """Scrape country population data from Wikipedia"""
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    
    print(f"Scraping data from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    
    rows_data = []
    
    for tr in table.find_all('tr')[1:]:
        cells = tr.find_all(['td', 'th'])
        if len(cells) >= 3:
            try:
                rank = cells[0].get_text(strip=True)
                country_cell = cells[1]
                country = country_cell.get_text(strip=True)
                population = cells[2].get_text(strip=True)
                percentage = cells[3].get_text(strip=True) if len(cells) > 3 else ''
                date = cells[4].get_text(strip=True) if len(cells) > 4 else ''
                source = cells[5].get_text(strip=True) if len(cells) > 5 else ''
                
                rows_data.append({
                    'rank': rank,
                    'country': country,
                    'population': population,
                    'percentage': percentage,
                    'date': date,
                    'source': source
                })
            except Exception:
                continue
    
    df = pd.DataFrame(rows_data)
    print(f"Scraped {len(df)} rows of data")
    return df

def clean_data(df):
    """Clean and transform the scraped data"""
    print("\nCleaning data...")
    print(f"Initial rows: {len(df)}")
    
    initial_count = len(df)
    df = df[df['country'].notna() & (df['country'] != '')]
    print(f"Step 1: Removed {initial_count - len(df)} rows with missing country names")
    
    def clean_population(pop_str):
        if pd.isna(pop_str) or pop_str == '':
            return None
        pop_str = str(pop_str).replace(',', '')
        pop_str = re.sub(r'\[.*?\]', '', pop_str)
        pop_str = re.sub(r'\(.*?\)', '', pop_str)
        pop_str = re.sub(r'[^\d.]', '', pop_str)
        return pop_str.strip()
    
    df['population'] = df['population'].apply(clean_population)
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    print(f"Step 2: Converted population to numeric (valid: {df['population'].notna().sum()})")
    
    def clean_percentage(pct_str):
        if pd.isna(pct_str) or pct_str == '':
            return None
        pct_str = str(pct_str).replace('%', '').strip()
        pct_str = re.sub(r'\[.*?\]', '', pct_str)
        return pct_str.strip()
    
    df['percentage'] = df['percentage'].apply(clean_percentage)
    df['percentage'] = pd.to_numeric(df['percentage'], errors='coerce')
    print("Step 3: Converted percentage to numeric")
    
    for col in ['rank', 'country', 'date', 'source']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].apply(lambda x: re.sub(r'\[.*?\]', '', str(x)))
    print("Step 4: Trimmed whitespace and removed citations from text columns")
    
    before_filter = len(df)
    df = df[df['population'].notna() & (df['population'] > 0)]
    print(f"Step 5: Removed {before_filter - len(df)} rows with invalid population")
    
    print(f"\nFinal dataset contains {len(df)} valid rows")
    return df

def produce_to_kafka(df, topic_name, bootstrap_servers='localhost:9092'):
    """Send each row to Kafka as a JSON message"""
    print(f"\nConnecting to Kafka at {bootstrap_servers}...")
    
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        
        print(f"Connected! Producing messages to topic: {topic_name}")
        success_count = 0
        for idx, row in df.iterrows():
            message = row.to_dict()
            for key, value in message.items():
                if pd.isna(value):
                    message[key] = None
                elif hasattr(value, 'item'):
                    message[key] = value.item()
            try:
                future = producer.send(topic_name, value=message)
                future.get(timeout=10)
                success_count += 1
                if success_count % 50 == 0:
                    print(f"Sent {success_count} messages...")
            except KafkaError as e:
                print(f"Failed to send message for {message.get('country', 'unknown')}: {e}")
        
        producer.flush()
        producer.close()
        print(f"Successfully sent {success_count}/{len(df)} messages to Kafka")
        return success_count
        
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        print("Make sure Kafka is running on localhost:9092")
        return 0

def save_data(df, csv_path='cleaned_data.csv', json_path='cleaned_data.json'):
    """Save cleaned data to CSV and JSON files"""
    print("\nSaving data to files...")
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV: {csv_path} ({len(df)} rows)")
    df.to_json(json_path, orient='records', indent=2)
    print(f"Saved JSON: {json_path}")

def main():
    """Main pipeline execution"""
    print("=" * 70)
    print("DATA PIPELINE: Wikipedia Countries → Kafka")
    print("=" * 70)
    
    username = "23B030310"
    topic_name = f"bonus_{username}"
    
    print(f"\nKafka Topic: {topic_name}")
    
    print("\n" + "─" * 70)
    print("STEP 1: SCRAPING DATA")
    print("─" * 70)
    df = scrape_wikipedia_population()
    
    print("\n" + "─" * 70)
    print("STEP 2: CLEANING DATA")
    print("─" * 70)
    df_cleaned = clean_data(df)
    
    if len(df_cleaned) == 0:
        print("\nERROR: No valid data after cleaning!")
        return
    
    print("\n" + "─" * 70)
    print("SAMPLE DATA (First 5 rows):")
    print("─" * 70)
    print(df_cleaned.head(5).to_string(index=False))
    
    print("\n" + "─" * 70)
    print("STEP 3: PRODUCING TO KAFKA")
    print("─" * 70)
    produce_to_kafka(df_cleaned, topic_name)
    
    print("\n" + "─" * 70)
    print("STEP 4: SAVING FILES")
    print("─" * 70)
    save_data(df_cleaned)
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print("\nSample Kafka message:")
    print("─" * 70)
    sample = df_cleaned.iloc[0].to_dict()
    print(json.dumps(sample, indent=2, default=str))
    
    print("\nTo consume messages from Kafka:")
    print(f"  kafka-console-consumer.sh --bootstrap-server localhost:9092 \\")
    print(f"    --topic {topic_name} --from-beginning")

if __name__ == "__main__":
    main()
