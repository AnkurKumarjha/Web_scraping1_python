# Web Scraping: Largest US Companies by Revenue

A Python script that scrapes the Wikipedia table of the largest companies in the United States by revenue and saves it as a CSV.

## Overview

The script requests a Wikipedia page, parses it with BeautifulSoup, pulls out the target data table, and writes it to a local CSV file using pandas.

**Data source:** [List of largest companies in the United States by revenue, Wikipedia](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue)

As of writing, that table lists the top 100 US companies by revenue (Fortune 500, fiscal year 2024 data) with the columns: Rank, Name, Industry, Revenue (USD millions), Revenue growth, Employees, and Headquarters. Since Wikipedia updates this page periodically, re-running the script later will pick up whatever data is live at the time.

## How It Works

1. **Fetch the page**: sends a GET request to the Wikipedia article, with a custom `User-Agent` header (Wikipedia blocks the default `python-requests` user agent).
2. **Parse the HTML**: loads the response into BeautifulSoup.
3. **Locate the table**: finds the first table on the page with the class `wikitable sortable`.
4. **Extract column headers**: pulls all `<th>` text from the table, filtering out any that are purely numeric.
5. **Extract row data**: for every table row after the header, grabs all `<td>` cell text and appends it to a pandas DataFrame.
6. **Save to CSV**: writes the finished DataFrame to disk.

## Usage

1. Open `web_scrapping.py` and update the output path at the bottom to a location on your machine:
   ```python
   df.to_csv(r"C:\Users\Ankur\Documents\python\companies.csv", index=False)
   ```
2. Run the script:
   ```bash
   python web_scrapping.py
   ```
3. Check the output path for `companies.csv`.

## Script

```python
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Request Wikipedia page content
url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
headers = {"User-Agent": "Mozilla/5.0"}
path = requests.get(url, headers=headers)

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(path.text, "html.parser")

# Find the target table
table = soup.find("table", class_="wikitable sortable")

# Extract column headers
world_titles = table.find_all("th")
table_titles = [title.text for title in world_titles]
column_titles = []
for titles in table_titles:
    if not titles.isdigit():
        column_titles.append(titles)

# Initialize pandas DataFrame
df = pd.DataFrame(columns=column_titles)

# Extract row data and append to DataFrame
column_data = table.find_all("tr")
for row in column_data[1:]:
    row_data = row.find_all("td")
    individual_row_data = [data.text.strip() for data in row_data]
    length = len(df)
    df.loc[length] = individual_row_data

# Save DataFrame to CSV
df.to_csv(r"C:\Users\Ankur\Documents\python\companies.csv", index=False)
```

## Notes

- The output path (`C:\Users\Ankur\Documents\python\companies.csv`) is hardcoded to a specific Windows user directory. Update it before running the script on a different machine.
- `soup.find(...)` grabs the *first* table matching `wikitable sortable` on the page. If Wikipedia ever adds another sortable table earlier in the article, the script would scrape the wrong one, worth a quick check if the output looks off.
- The `.isdigit()` filter on headers is there to drop per-row rank numbers that Wikipedia sometimes marks up as header cells (`<th>`) rather than data cells (`<td>`), so they don't get mistaken for genuine column names. If the live page happens to mark the Rank column that way, the header list will include a "Rank" entry with no matching `<td>` value in each row, which would make the row-assignment step fail with a length mismatch. If you hit that error, drop "Rank" from `column_titles` (or extract it separately) before assigning rows.
- Wikipedia's page structure and content can change at any time; if the script stops working, the table's class name or position on the page is the first thing to check.

## Files in This Repo

| File | Description |
|---|---|
| `web_scrapping.py` | The scraping script |
| `requirements.txt` | Python packages required to run the script |
| `README.md` | Project documentation (this file) |
| `companies.csv` | Scraped output: largest US companies by revenue, snapshot at time of scraping |

## Tech Stack

- **Language:** Python 3
- **Libraries:** `requests`, `beautifulsoup4`, `pandas`
