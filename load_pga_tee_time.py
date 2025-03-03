import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL of the webpage to scrape
url = 'https://www.pgatour.com/tee-times'

# Send a GET request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the script tag containing JSON data
script_tag = soup.find('script', {'type': 'application/json'})
json_data = json.loads(script_tag.string)

# Extract tee times data
tee_times_data = json_data['props']['pageProps']['teeTimes']['rounds']

# Extract relevant data
data = []
for round_info in tee_times_data:
    for group in round_info['groups']:
        group_info = {
            'Group Number': group['groupNumber'],
            'Tee Time': pd.to_datetime(group['teeTime'], unit='ms'),
            'Start Tee': group['startTee'],
            'Group Location': group['groupLocation'],
            'Group Hole': group['groupHole'],
            'Course Name': group['courseName'],
            'Group Status': group['groupStatus'],
        }
        for player in group['players']:
            player_info = {
                **group_info,
                'Player Name': player['displayName'],
                'Country': player['country'],
            }
            data.append(player_info)

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head(2))
