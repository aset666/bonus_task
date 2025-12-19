# Real-Time Car Park Analytics Pipeline

## 📖 Project Overview
[cite_start]This project implements a robust data engineering pipeline to monitor and analyze car park occupancy in New South Wales (NSW)[cite: 263]. [cite_start]Using the **Transport for NSW Car Park API**, the system ingests live data via **Kafka**, processes it with **Airflow**, and stores refined metrics in an **SQLite** database for daily reporting[cite: 266, 291].

## 👥 Team Members
1. **Smetov Damir**
2. **Ravshanbekov Assadbek**
3. **Yerken Yarmukhamed**

## 🏗 System Architecture
The pipeline is divided into three automated jobs:

1.  **Job 1: Ingestion (Real-Time)**
    * [cite_start]Fetches facility data every minute (e.g., TSN 2155384 for Tallawong)[cite: 373].
    * Produces raw JSON events to a Kafka topic.
2.  **Job 2: Cleaning & Storage**
    * [cite_start]Consumes Kafka messages and cleans data (handling nulls and type conversion)[cite: 318, 321].
    * [cite_start]Calculates availability using the formula: $Availability = spots - total$.
    * Stores cleaned records in SQLite.
3.  **Job 3: Daily Analytics**
    * Aggregates daily occupancy trends.
    * Identifies peak hours and average utilization.

## 🛠 Tech Stack
* **Orchestration:** Apache Airflow
* **Streaming:** Apache Kafka
* **Processing:** Python (Pandas)
* **Database:** SQLite
* **Environment:** GitHub Codespaces

## 🚀 Execution Instructions
1.  **Environment:** Open in GitHub Codespaces.
2.  **Services:** Start Zookeeper and Kafka broker.
3.  **Airflow:** Run `airflow standalone` or start the scheduler/webserver separately.
4.  **DAGs:** Unpause `job1_ingestion_dag`, `job2_clean_store_dag`, and `job3_daily_summary_dag`.

---

🚀 Installation & Quick Start🍎 For macOS (using Homebrew)Install Services:Bashbrew install kafka zookeeper
pip install -r requirements.txt
Start Infrastructure:Terminal 1 (Zookeeper): zookeeper-server-start /usr/local/etc/kafka/zookeeper.propertiesTerminal 2 (Kafka): kafka-server-start /usr/local/etc/kafka/server.propertiesLaunch Airflow:Bashexport AIRFLOW_HOME=$(pwd)/airflow
airflow standalone
🐧 For Linux (Ubuntu)Prerequisites:Bashsudo apt update && sudo apt install default-jdk -y
pip install apache-airflow pandas kafka-python
Setup Kafka:Download the Kafka binaries, extract them, and run:Terminal 1: bin/zookeeper-server-start.sh config/zookeeper.propertiesTerminal 2: bin/kafka-server-start.sh config/server.propertiesLaunch Airflow:Bashexport AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow standalone
📊 Pipeline Workflow (DAGs)JobNameFrequencyResponsibilityJob 1job1_ingestion_dagEvery 1 minPolls TfNSW API and produces messages to raw_events Kafka topic.Job 2job2_clean_store_dagHourlyConsumes Kafka, performs type casting, calculates availability ($Total - Occupancy$).Job 3job3_daily_summary_dagDaily @ 00:00Aggregates data in SQLite to find peak times and utilization rates.📂 Project StructureBash.
├── airflow/
│   └── dags/               # Orchestration logic (DAG definitions)
├── src/
│   ├── job1_producer.py    # Ingestion: API ➡️ Kafka
│   ├── job2_cleaner.py     # Processing: Kafka ➡️ SQLite
│   ├── job3_analytics.py   # Analytics: SQL Aggregations
│   └── db_utils.py         # Shared database utilities
├── data/
│   └── app.db              # Relational Storage (SQLite)
└── requirements.txt        # Environment dependencies
