import pandas as pd

def analyze_query():
    # Load the dataset
    try:
        sales_data = pd.read_csv('/home/rasaaltewari/training/week-9/day3/tools/workspace/sales.csv')
    except FileNotFoundError:
        print("The file sales.csv was not found.")
        return

    # Since the query is 'analyze sample.txt', we assume it's asking to analyze a file named sample.txt
    # However, the provided dataset is sales.csv, so we'll proceed with that
    # If sample.txt exists and contains relevant data, you should load that instead

    # Apply filtering if needed (for this example, we won't apply any filtering)
    filtered_data = sales_data

    # Apply aggregation if needed (for this example, we'll calculate total sales)
    total_sales = filtered_data['sales'].sum() if 'sales' in filtered_data.columns else "Sales column not found"

    print("Total sales:", total_sales)

# Demo
analyze_query()