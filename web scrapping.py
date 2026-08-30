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