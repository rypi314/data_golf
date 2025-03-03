import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL of the webpage to scrape
url = 'https://www.pgatour.com/fedexcup'

# Send a GET request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the leaderboard data
table = soup.find('table', {'class': 'table-styled'})

# Ensure the table is found
if table is None:
    raise ValueError("Leaderboard table not found")

# Find all the rows in the table
rows = table.find_all('tr')[1:]  # Skip the header row

# Extract relevant data
data = []
for row in rows:
    cols = row.find_all('td')
    rank = cols[0].text.strip()
    player_name = cols[1].text.strip()
    points = cols[2].text.strip()
    events = cols[3].text.strip()
    wins = cols[4].text.strip()
    top10s = cols[5].text.strip()

    player_info = {
        'Rank': rank,
        'Player Name': player_name,
        'Points': points,
        'Events': events,
        'Wins': wins,
        'Top 10s': top10s,
    }
    data.append(player_info)

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head(10))
