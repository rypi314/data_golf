import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
})

# Convert DataFrame to Markdown format
markdown_table = df.to_markdown(index=False)

# Write to a Markdown file
with open("data.md", "w") as f:
    f.write(markdown_table)

print("Markdown file created: data.md")
