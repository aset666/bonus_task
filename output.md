1)
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

2)
(venv) C:\Users\User\Desktop\bonus task>docker ps -a
CONTAINER ID   IMAGE                                    COMMAND                  CREATED       STATUS                  PORTS                                         NAMES
6321bf84e9e1   confluentinc/cp-kafka:7.5.0              "/etc/confluent/dock…"   2 hours ago   Up 2 hours              0.0.0.0:9092->9092/tcp, [::]:9092->9092/tcp   0186f8bb7403_bonustask-kafka
7b1bc938995d   confluentinc/cp-zookeeper:7.5.0          "/etc/confluent/dock…"   2 hours ago   Up 2 hours              0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   bonustask-zookeeper 
b72c33476a87   learning-airflow_3cdb78/airflow:latest   "tini -- /entrypoint…"   4 days ago    Up 2 hours                                                            learning-airflow_3cdb78-triggerer-1
ffe365370540   learning-airflow_3cdb78/airflow:latest   "tini -- /entrypoint…"   4 days ago    Up 2 hours                                                            learning-airflow_3cdb78-scheduler-1
e75d305d14a8   learning-airflow_3cdb78/airflow:latest   "tini -- /entrypoint…"   4 days ago    Up 2 hours                                                            learning-airflow_3cdb78-dag-processor-1
9d7b6219fed1   learning-airflow_3cdb78/airflow:latest   "tini -- /entrypoint…"   4 days ago    Up 2 hours              127.0.0.1:8080->8080/tcp                      learning-airflow_3cdb78-api-server-1
c87a2efd972f   learning-airflow_3cdb78/airflow:latest   "tini -- /entrypoint…"   4 days ago    Exited (0) 4 days ago                                                 learning-airflow_3cdb78-db-migration-1
62a6dcbab527   postgres:12.6                            "docker-entrypoint.s…"   6 days ago    Up 2 hours              127.0.0.1:5432->5432/tcp                      learning-airflow_3cdb78-postgres-1


3){"rank": "World", "country": "8,232,000,000", "population": 100.0, "percentage": null, "date": "UN projection", "source": ""}
{"rank": "India", "country": "1,417,492,000", "population": 17.3, "percentage": null, "date": "Official projection", "source": ""}
{"rank": "China", "country": "1,408,280,000", "population": 17.1, "percentage": null, "date": "Official estimate", "source": ""}
{"rank": "United States", "country": "340,110,988", "population": 4.1, "percentage": null, "date": "Official estimate", "source": ""}
{"rank": "Indonesia", "country": "284,438,782", "population": 3.5, "percentage": null, "date": "National annual projection", "source": ""}
{"rank": "Pakistan", "country": "241,499,431", "population": 2.9, "percentage": null, "date": "2023 census result", "source": ""}
{"rank": "Nigeria", "country": "223,800,000", "population": 2.7, "percentage": null, "date": "Official projection", "source": ""}
...

