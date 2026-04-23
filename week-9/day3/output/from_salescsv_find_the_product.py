import pandas as pd

# Load dataset
df = pd.read_csv("/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv")

# Print column names
print("Columns:", df.columns)

# Detect column names dynamically
cols = [c.lower() for c in df.columns]

# Find region, product, and units columns
region_col = next((c for c in df.columns if "region" in c.lower()), None)
product_col = next((c for c in df.columns if "product" in c.lower()), None)
units_col = next((c for c in df.columns if c.lower() in ["units", "quantity"]), None)

# Check if required columns exist
if not region_col or not product_col or not units_col:
    print("Required columns not found")
else:
    # Filter data for south region
    south_region_df = df[df[region_col].str.lower() == "south"]
    
    # Group by product and sum units
    product_units = south_region_df.groupby(product_col)[units_col].sum().reset_index()
    
    # Find product with lowest units sold
    lowest_units_product = product_units.loc[product_units[units_col].idxmin()]
    
    # Print result
    print("Product with lowest units sold in south region:")
    print(f"Product: {lowest_units_product[product_col]}")
    print(f"Units Sold: {lowest_units_product[units_col]}")