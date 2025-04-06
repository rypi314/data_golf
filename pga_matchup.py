import load_pga_tee_time
#import load_world_rank
import pandas as pd
from datetime import datetime, timedelta

# Load the pga tee times 
df_tee_time = load_pga_tee_time.df

# Convert user input to a pandas Timestamp
date_input = pd.to_datetime(datetime.now())
# Filter the DataFrame to include only rows with the specified date
df_tee_time = df_tee_time[df_tee_time['Tee Time'].dt.date == date_input.date()]

df_world_rank = pd.read_csv('rankings_list.csv')

df_times_rank = pd.merge(df_tee_time, df_world_rank, left_on='Player Name', right_on='Full Name', how='left')

df_times_rank = df_times_rank[['Group Number','Tee Time', 'Course Name', 'Player Name'
                               #,'Official Rank'
                               ,'Rank']]

# Group by the key and calculate the difference between rows
# Calculate the maximum value for each 'Group Number' group
max_values = df_times_rank.groupby('Group Number')['Rank'].transform('min')

# Calculate the difference between the maximum and each value
df_times_rank['Difference'] = max_values - df_times_rank['Rank']

df_best_groups = df_times_rank[df_times_rank['Difference']<0]

# Filter rows in df_other based on Group Numbers in df_best_groups
df_bet = df_times_rank[df_times_rank['Group Number'].isin(df_best_groups['Group Number'])]

# Compute the mean for each group and assign it as a new column
df_bet['Sum'] = df_bet.groupby('Group Number')['Difference'].transform('sum')
df_bet['Average'] = df_bet.groupby('Group Number')['Difference'].transform('mean').round(decimals=1)

df_print = df_bet.sort_values(by='Sum', ascending=True).head(n=12)

print(df_print)


# Find player with the lowest rank for each tee time group
lowest_ranked_players = df_print.loc[df_print.groupby("Tee Time")["Rank"].idxmin()]

# Calculate sum and average of differences for each group
grouped_data = df_print.groupby("Tee Time")["Difference"].agg(["sum", "mean"]).reset_index()
lowest_ranked_players = lowest_ranked_players.merge(grouped_data, on="Tee Time")

course_str = df_print['Course Name'].head(n=1).values[0]

# Generate paragraph summary
summary = f"For each tee time grouping at {course_str}, the player with the lowest rank has been identified along with key performance metrics.\n"
for _, row in lowest_ranked_players.iterrows():
    summary += (f"* In the group that teed off at {row['Tee Time']}, **{row['Player Name']}** holds the lowest rank."
                f"This group collectively has a combined rank of {row['sum']*-1}, "
                f"leading to an average difference in rank of {row['mean']*-1:.1f} across its members. \n ")

print(summary)