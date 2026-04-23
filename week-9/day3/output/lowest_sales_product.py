import pandas as pd

# Load the dataset
df = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')

# Find the product with the lowest units sold
lowest_sales_product = df.loc[df['units_sold'].idxmin()]['product']

# Print the final answer
print("The product with the lowest units sold is:", lowest_sales_product)