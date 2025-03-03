import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = 'https://www.pgatour.com/fedexcup.html'

# Send a GET request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the script tag containing JSON data
script_tag = soup.find('script', {'type': 'application/json'})

# Extract the JSON data
if script_tag:
    json_data = json.loads(script_tag.string)
    # Extract FedExCup rank data
    fedex_rank_data = json_data['props']['pageProps']['tourCupDetails']['projectedPlayers']
    
    # Print each player's display name if it exists
    for player in fedex_rank_data:
        if 'displayName' in player:
            print(player['displayName'])
        else:
            print('displayName key not found for this player.')
else:
    print('Script tag with JSON data not found.')
