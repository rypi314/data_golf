import requests
import json

# API URL
url = "https://apiweb.owgr.com/api/owgr/rankings/getRankings?regionId=0&pageSize=100&pageNumber=1&countryId=0&sortString=Rank+ASC"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()
    
    # Save the JSON data to a file
    with open('rankings.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print("JSON data has been saved to 'rankings.json'.")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
