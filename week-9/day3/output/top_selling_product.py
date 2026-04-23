import pandas as pd

def top_selling_product_north():
    # Load the dataset
    sales = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')

    # Filter sales data for North region
    north_sales = sales[sales['region'] == 'North']

    # Group by product and sum units sold
    product_sales = north_sales.groupby('product')['units_sold'].sum().reset_index()

    # Find the product with the highest units sold
    top_product = product_sales.loc[product_sales['units_sold'].idxmax()]

    # Print the final answer
    print("The product with the highest units sold in the North region is:", top_product['product'])

# Execute the function
top_selling_product_north()