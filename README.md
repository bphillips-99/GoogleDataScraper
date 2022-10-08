# Google Trends Data Scraper
Python script to collect Google Trends weekly, daily, monthly, and yearly data with for a keyword save results in a csv file.

## Requirements
Install packages required to run script
```bash
$ pip install -r requirements.txt
```
## Usage
### Parameters
* **frequency**: Frequency of data points (D,W,M,Y)
* **keyword**: Keyword to used to collect trend data
    * Default 'bitcoin'
* **filename**: File location and name. Saved as CSV
* **startDate**: First date of data inclusive
    * Format '%Y-%m-%d'
* **endDate**: Last date of data inclusive
    * Format '%Y-%m-%d'
### Sample
```bash
$ py DataScraper.py --frequency=D --keyword=bitcoin
```

