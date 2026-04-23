import pandas as pd

def get_best_selling_product():
    # Load the dataset
    sales_data = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')
    
    # Assuming 'product' and 'units_sold' are the column names for product and units sold respectively
    # Filter out any rows with missing or non-numeric values in 'units_sold'
    sales_data = sales_data[pd.to_numeric(sales_data['units_sold'], errors='coerce').notnull()]
    sales_data['units_sold'] = pd.to_numeric(sales_data['units_sold'])
    
    # Group by 'product' and sum 'units_sold', then find the product with the highest units sold
    best_selling_product = sales_data.groupby('product')['units_sold'].sum().idxmax()
    
    return best_selling_product

# Demo
print("The product with the highest units sold is:", get_best_selling_product())