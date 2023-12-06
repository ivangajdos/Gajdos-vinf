import pandas as pd

def merge_csv_files(csv_file1, csv_file2, common_column, output_csv):
    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    # Merge DataFrames based on the common column
    merged_df = pd.merge(df1, df2, on=common_column)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_csv, index=False)

    print(f"Merged data saved to {output_csv}")

# Example usage
csv_file1 = 'matches.csv'  # Replace with the path to your first CSV file
csv_file2 = 'stadiums.csv'  # Replace with the path to your second CSV file
common_column = 'home'  # Replace with the common column name
output_csv = 'merged_output.csv'  # Replace with the desired output file name

merge_csv_files(csv_file1, csv_file2, common_column, output_csv)