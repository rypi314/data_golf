import load_pga_tee_time
import load_world_rank
import pandas as pd

df_tee_time = load_pga_tee_time.df

# User input for the date
# Need try catch if date is old tournament.

from datetime import datetime, timedelta

# Get current time
now = datetime.now()
# Check if it's AM or PM
if now.hour < 12:
    result_date = now.date()  # Today's date
else:
    result_date = (now + timedelta(days=1)).date()  # Tomorrow's date

date_input = result_date

# Convert user input to a pandas Timestamp
date_input = pd.to_datetime(date_input)

# Filter the DataFrame to include only rows with the specified date
df_tee_time = df_tee_time[df_tee_time['Tee Time'].dt.date == date_input.date()]

df_world_rank = load_world_rank.df

df_times_rank = pd.merge(df_tee_time, df_world_rank, left_on='Player Name', right_on='Full Name', how='left')

df_times_rank = df_times_rank[['Group Number','Tee Time', 'Player Name'
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

df_print = df_bet.sort_values(by='Sum', ascending=True).head(n=10)

# Compute column widths
col_widths = {col: max(df_print[col].astype(str).map(len).max(), len(col)) for col in df_print.columns}
# Generate Markdown table
header = "| " + " | ".join([f"{col:<{col_widths[col]}}" for col in df_print.columns]) + " |"
separator = "|-" + "-|-".join(["-" * col_widths[col] for col in df_print.columns]) + "-|"
rows = "\n".join(["| " + " | ".join([f"{str(row[col]):<{col_widths[col]}}" for col in df_print.columns]) + " |" for _, row in df_print.iterrows()])

markdown_table = f"{header}\n{separator}\n{rows}"

print(markdown_table)
#df_print.head(n=10)