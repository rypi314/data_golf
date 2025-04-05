import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
})

# Compute column widths
col_widths = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}

# Generate Markdown table
header = "| " + " | ".join([f"{col:<{col_widths[col]}}" for col in df.columns]) + " |"
separator = "|-" + "-|-".join(["-" * col_widths[col] for col in df.columns]) + "-|"
rows = "\n".join(["| " + " | ".join([f"{str(row[col]):<{col_widths[col]}}" for col in df.columns]) + " |" for _, row in df.iterrows()])

markdown_table = f"{header}\n{separator}\n{rows}"

print(markdown_table)