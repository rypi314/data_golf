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

# Extract fedex rank data
fedex_rank_data = json_data['props']['pageProps']['tourCupDetails']['projectedPlayers']

# Extract relevant data
data = []
for player in fedex_rank_data:
    player_info = {
        'Player Name': player.get('displayName', 'N/A'),
        'Country': player.get('country', 'N/A'),
        'Projected Rank': player.get('rankingData', {}).get('projected', 'N/A'),
        'Official Rank': player.get('rankingData', {}).get('official', 'N/A'),
        'Point Data Projected': player.get('pointData', {}).get('projected', 'N/A'),
        'Point Data Official': player.get('pointData', {}).get('official', 'N/A')
    }
    data.append(player_info)

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head(2))
