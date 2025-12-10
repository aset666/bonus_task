C:\Users\User\Desktop\bonus task>venv\Scripts\activate

(venv) C:\Users\User\Desktop\bonus task>python script.py
======================================================================
DATA PIPELINE: Wikipedia Countries → Kafka
======================================================================

Kafka Topic: bonus_23B030310

──────────────────────────────────────────────────────────────────────
STEP 1: SCRAPING DATA
──────────────────────────────────────────────────────────────────────
Scraping data from: https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
Scraped 240 rows of data

──────────────────────────────────────────────────────────────────────
STEP 2: CLEANING DATA
──────────────────────────────────────────────────────────────────────

Cleaning data...
Initial rows: 240
Step 1: Removed 0 rows with missing country names
Step 2: Converted population to numeric (valid: 240)
Step 3: Converted percentage to numeric
Step 4: Trimmed whitespace and removed citations from text columns
Step 5: Removed 11 rows with invalid population

Final dataset contains 229 valid rows

──────────────────────────────────────────────────────────────────────
SAMPLE DATA (First 5 rows):
──────────────────────────────────────────────────────────────────────
         rank       country  population  percentage                       date source
        World 8,232,000,000       100.0         NaN              UN projection       
        India 1,417,492,000        17.3         NaN        Official projection       
        China 1,408,280,000        17.1         NaN          Official estimate       
United States   340,110,988         4.1         NaN          Official estimate
    Indonesia   284,438,782         3.5         NaN National annual projection

──────────────────────────────────────────────────────────────────────
STEP 3: PRODUCING TO KAFKA
──────────────────────────────────────────────────────────────────────

Connecting to Kafka at localhost:9092...
Connected! Producing messages to topic: bonus_23B030310
Sent 50 messages...
Sent 100 messages...
Sent 150 messages...
Sent 200 messages...
Successfully sent 229/229 messages to Kafka

──────────────────────────────────────────────────────────────────────
STEP 4: SAVING FILES
──────────────────────────────────────────────────────────────────────

Saving data to files...
Saved CSV: cleaned_data.csv (229 rows)
Saved JSON: cleaned_data.json

======================================================================
PIPELINE COMPLETED SUCCESSFULLY!
======================================================================

Sample Kafka message:
──────────────────────────────────────────────────────────────────────
{
  "rank": "World",
  "country": "8,232,000,000",
  "population": 100.0,
  "percentage": NaN,
  "date": "UN projection",
  "source": ""
}

To consume messages from Kafka:
  kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic bonus_23B030310 --from-beginning
