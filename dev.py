from datetime import datetime, timedelta
import pandas as pd

# Convert user input to a pandas Timestamp
date_input = pd.to_datetime(datetime.now().date())

print(date_input)