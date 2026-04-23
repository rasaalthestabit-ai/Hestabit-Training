import pandas as pd

def highest_revenue_product():
    # Load the dataset
    sales_data = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')

    # Filter data for South region
    south_region_data = sales_data[sales_data['region'] == 'South']

    # Group by product and calculate total revenue
    product_revenue = south_region_data.groupby('product')['revenue'].sum().reset_index()

    # Find the product with the highest revenue
    highest_revenue_product = product_revenue.loc[product_revenue['revenue'].idxmax()]

    # Print the final answer
    print("The product with the highest revenue in the South region is:", highest_revenue_product['product'])

# Call the function
highest_revenue_product()