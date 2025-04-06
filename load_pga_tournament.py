import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage to scrape
url = 'https://www.pgatour.com/leaderboard'

# Send a GET request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the script tag containing JSON data
script_tag = soup.find('script', {'id': 'leaderboard-seo-data'})
json_data = script_tag.string

# Parse JSON data
import json
data = json.loads(json_data)

# Extract column names
column_names = [col['csvw:name'] for col in data['mainEntity']['csvw:tableSchema']['csvw:columns']]

# Extract data for each column
columns_data = {}
for col in data['mainEntity']['csvw:tableSchema']['csvw:columns']:
    column_name = col['csvw:name']
    column_data = [cell['csvw:value'] for cell in col['csvw:cells']]
    columns_data[column_name] = column_data

# Create a DataFrame
df = pd.DataFrame(columns_data)

# Convert the columns to numeric values using to_numeric with errors='coerce' to handle non-numeric values
df[['R1', 'R2', 'R3', 'R4']] = df[['R1', 'R2', 'R3', 'R4']].apply(pd.to_numeric, errors='coerce')

# Calculate total strokes by summing the rows
df['total_stroke'] = df[['R1', 'R2', 'R3', 'R4']].sum(axis=1).astype(int)

# Replace null values with '-' 
df.fillna('-', inplace=True)

# Display the DataFrame
print(df.head(2))
