import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL of the webpage to scrape
url = 'https://www.pgatour.com/fedexcup'

# Send a GET request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the script tag containing JSON data
script_tag = soup.find('script', {'type': 'application/json'})
json_data = json.loads(script_tag.string)

# Extract tee times data
fedex_rank_data = json_data['props']['pageProps']['tourCupDetails']['projectedPlayers']

# Extract relevant data
data = []
for player in json_data:
    player_info = {
        'Player Name': player['displayName'],
        'Country': player['country'],
        'Projected Rank': player['rankingData']['projected'],
        'Official Rank': player['rankingData']['official'],
        'Point Data Projected': player['pointData']['projected'],
        'Point Data Official': player['pointData']['official']
    }
    data.append(player_info)

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head(10))
