# bonus_task
BONUS_TASK: WEBsite to Kafka
my website:
Wikipedia Countries → Kafka
URL:
https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
The website about countries with their population

Scraping
I use libraries request and BeautifulSoup
requests for HTTP requests
BeautifulSoup for parsing HTML
proces of scraping:
Sent a GET request to the Wikipedia page with a proper User-Agent header.
Parsed the HTML content using BeautifulSoup.
Selected the main table with the class wikitable.
Columns in the table:
1)rank — country rank by population
2)country — country name
3)population — population count (absolute numbers)
4)percentage — share of world population (%)
5)date — date of estimate or projection
6)source — source of data
Total rows scraped: 240

Data Cleaning Steps
Removed rows with missing country names (0 rows removed)
Converted population column to numeric and removed unwanted characters (commas, brackets, citations)
Converted percentage column to numeric, removed % symbols and citations
Trimmed whitespace and removed citations from text columns (rank, country, date, source)
Removed rows with invalid or missing population values (11 rows removed)
Final dataset contains 229 valid rows

Kafka production i use kafka-python
topic name bonus_23B030310 my ID
the process
connected to Kafka running on localhost:9092.
produced each row as a JSON message.
successfully sent 229 messages to Kafka.
Example Kafka Message
{
  "rank": "World",
  "country": "8,232,000,000",
  "population": 100.0,
  "percentage": null,
  "date": "UN projection",
  "source": ""
}

I verified messages by consuming the Kafka topic using:
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bonus_23B030310 --from-beginning
And if you want run the script
1. activate virt. env. for windows:venv\Scripts\activate
2. Run the script: python script.py
3. After running, the script will:
scrape and clean data from Wikipedia
produce each row to Kafka as a JSON message
save cleaned data to cleaned_data.csv and cleaned_data.json
checking Messages in Kafka
docker exec -it 0186f8bb7403_bonustask-kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bonus
for kafka use docker
install docker and run it, create docker-compose.yml file and write from documentation kafka 

