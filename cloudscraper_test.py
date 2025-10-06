import os
import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd

# URL (change for each table)
url = "https://fbref.com/en/squads/53a2f082/2023-2024/Real-Madrid-Stats"

# Create a scraper that bypasses Cloudflare
scraper = cloudscraper.create_scraper()

# Download the webpage
response = scraper.get(url)
if response.status_code != 200:
    raise Exception(f"The webpage could not be accessed: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Search only for the div of the all_stats_standard table
div = soup.find("div", {"id": "all_stats_standard"})
if not div:
    raise Exception("The all_stats_standard table was not found on the website")

# Check whether the table is in comments
comments = div.find_all(string=lambda text: isinstance(text, Comment))
table = None

for c in comments:
    comment_soup = BeautifulSoup(c, "html.parser")
    candidate = comment_soup.find("table")
    if candidate:
        table = candidate
        break

# If the table is not in comments, scrape directly
if not table:
    table = div.find("table")

if not table:
    raise Exception("No table found in all_stats_standard")

# ---------------------------
# Process headers
# ---------------------------
thead = table.find("thead")
header_rows = thead.find_all("tr")
last_header = header_rows[-1]  # last row with real names
headers = [th.get_text(strip=True) for th in last_header.find_all("th")]

# ---------------------------
# Process data rows
# ---------------------------
rows = []
for row in table.find_all("tr"):
    # Player name in <th>
    th = row.find("th")
    player = th.get_text(strip=True) if th else None
    
    # Other columns in <td>
    cols = [td.get_text(strip=True) for td in row.find_all("td")]
    
    if cols:  # only rows with data
        rows.append([player] + cols)

# Ensure that ‘Player’ is the first column
if headers[0] != "Player":
    headers = ["Player"] + headers[1:]

# Create DataFrame
df = pd.DataFrame(rows, columns=headers[:len(rows[0])])

# ---------------------------
# Save CSV to ./tables folder
# ---------------------------
os.makedirs("./tables", exist_ok=True)
output_path = "./tables/all_stats_standard_rm_2324.csv"
df.to_csv(output_path, index=False)

print(f"✅ all_stats_standard table stored on {output_path}")
print(df.head())
