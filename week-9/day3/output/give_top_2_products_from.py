import pandas as pd

# Load dataset
df = pd.read_csv("/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv")

# Print column names
print("Columns:", df.columns)

# Convert column names to lowercase for safe detection
cols = [c.lower() for c in df.columns]

# Detect product and units columns
product_col = next((c for c in df.columns if "product" in c.lower()), None)
units_col = next((c for c in df.columns if c.lower() in ["units", "quantity"]), None)

# Check if required columns are found
if not product_col or not units_col:
    print("Required columns not found")
else:
    # Group by product and sum units, then sort in descending order
    result = df.groupby(product_col)[units_col].sum().sort_values(ascending=False)
    
    # Print top 2 products
    print("Top 2 products by units sold:")
    print(result.head(2))