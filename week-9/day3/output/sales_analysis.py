import pandas as pd

def analyze_sales_data(file_path):
    # Load the CSV file
    sales_data = pd.read_csv(file_path)

    # Compute top 5 products by revenue
    top_products = sales_data.groupby('product')['revenue'].sum().reset_index()
    top_products = top_products.sort_values(by='revenue', ascending=False).head(5)
    print("Top 5 Products by Revenue:")
    print(top_products)

    # Compute top region by units
    top_region = sales_data.groupby('region')['units'].sum().reset_index()
    top_region = top_region.sort_values(by='units', ascending=False).head(1)
    print("\nTop Region by Units:")
    print(top_region)

    # Compute total revenue
    total_revenue = sales_data['revenue'].sum()
    print("\nTotal Revenue: $", total_revenue)

# Demo
analyze_sales_data('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')