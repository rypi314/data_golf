import requests
import pandas as pd

# API URL
url = "https://apiweb.owgr.com/api/owgr/rankings/getRankings?regionId=0&pageSize=100&pageNumber=1&countryId=0&sortString=Rank+ASC"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()
    
    # Extract rankings list
    rankings_list = json_data.get("rankingsList", [])
    if not rankings_list:
        print("Rankings list data not found in the JSON.")
        exit()

    # Parse player data into a list of dictionaries
    data = []
    for entry in rankings_list:
        player = entry.get("player", {})
        country = player.get("country", {})
        
        # Extract relevant data
        player_info = {
            "Rank": entry.get("rank", "N/A"),
            "Full Name": player.get("fullName", "N/A"),
            "First Name": player.get("firstName", "N/A"),
            "Last Name": player.get("lastName", "N/A"),
            "Birth Date": player.get("birthDate", "N/A"),
            "Country": country.get("name", "N/A"),
            "Points Lost": entry.get("pointsLost", "N/A"),
            "Points Won": entry.get("pointsWon", "N/A"),
            "Points Total": entry.get("pointsTotal", "N/A"),
            "Points Average": entry.get("pointsAverage", "N/A"),
            "Last Week Rank": entry.get("lastWeekRank", "N/A"),
            "End Last Year Rank": entry.get("endLastYearRank", "N/A"),
            "Week End Date": entry.get("weekEndDate", "N/A")
        }
        data.append(player_info)

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # Display the first few rows of the DataFrame
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv('rankings_list.csv', index=False)
    print("Player rankings have been saved to 'rankings_list.csv'.")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
