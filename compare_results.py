import pandas as pd

def compare_csv_files(result_name1, result_name2, statistic='MEAN'):
    """
    Compare results of two CSV based on the statistic to see how it changed.

    Args:
        file1 (str): Path to the first CSV file.
        file2 (str): Path to the second CSV file.
        statistic (str): The statistic to compare (e.g., 'MEAN', 'STD').

    Returns:
        pd.DataFrame: DataFrame showing the comparison.
    """
    
    # Construct path to files
    file1 = "mialab/mia-result/" + result_name1 + "/results_summary.csv"
    file2 = "mialab/mia-result/"  + result_name2 + "/results_summary.csv"
    
    # Load the CSV files into pandas DataFrame
    df1 = pd.read_csv(file1, delimiter=';')
    df2 = pd.read_csv(file2, delimiter=';')

    # Filter by the specified statistic of interest
    df1_metric = df1[df1['STATISTIC'] == statistic]
    df2_metric = df2[df2['STATISTIC'] == statistic]

    # Merge (match) the two DataFrames depending on LABEL and METRIC
    comparison = pd.merge(
        df1_metric[['LABEL', 'METRIC', 'VALUE']],
        df2_metric[['LABEL', 'METRIC', 'VALUE']],
        on=['LABEL', 'METRIC'],
        suffixes=(str(result_name1), str(result_name2))
    )

    # Calculate differences from file2 to file1 (file2 - file1)
    comparison['DIFFERENCE'] = comparison.iloc[:,3] - comparison.iloc[:,2]

    return comparison


# When running this script __name__ will be set to "__main__" and execute bellow. 
# In case this script is used in another file (e.g. pipeline.py) then it will not be run.
if __name__ == "__main__":
    # File paths

    # Compare the files for the statistic 'MEAN'
    statistic = 'MEAN'
    result_name1="2024-11-21-21-30-11"
    result_name2= "2024-11-21-16-12-30"
    comparison_df = compare_csv_files(result_name1=result_name1,
                                      result_name2=result_name2,
                                      statistic=statistic)

    # Display the comparison DataFrame
    print("\nComparison:")
    print(comparison_df)

    # Save the comparison to a CSV file
    comparison_df.to_csv(path_or_buf=f'mialab/mia-result/{result_name1}/comparison_{statistic}.csv', index=False)
    print(f"\nComparison saved to mialab/mia-result/{result_name1}/comparison_{statistic}.csv")
