# 📊 fbref.com-scraping

This Python script scrapes player statistics from the [FBref](https://fbref.com) page and saves the `all_stats_standard` table as a CSV file.

## 🚀 Features

- Bypasses Cloudflare protections using `cloudscraper`
- Parses HTML and comments using `BeautifulSoup`
- Extracts the `all_stats_standard` table (even if hidden in HTML comments)
- Saves data to a structured CSV file in the `./tables/` folder

## 🧾 Output

- A CSV file: `./tables/all_stats_standard.csv`
- Contains player performance data (games, goals, assists, etc.)
