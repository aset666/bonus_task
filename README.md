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
