import pandas as pd

def analyze_sales():
    # Load the dataset
    try:
        sales_data = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')
    except FileNotFoundError:
        print("The file was not found. Please check the path.")
        return

    # Print basic information about the dataset
    print(sales_data.info())
    print(sales_data.describe())

# Execute the function
analyze_sales()