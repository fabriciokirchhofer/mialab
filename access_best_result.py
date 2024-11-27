import os
import pandas as pd
import datetime


def find_best_results(mia_result_dir, metric, brain_region, rank=1):
    """
    Finds the best results for a given metric and brain region across all results_summary.csv files.

    Args:
        mia_result_dir (str): Path to the mia-result folder.
        metric (str): Evaluation metric to rank (e.g., 'DICE', 'JACRD').
        brain_region (str): Brain region to focus on (e.g., 'WhiteMatter').
        rank (int): Rank to select (e.g., 1 for the best, 2 for second best).

    Returns:
        pd.DataFrame: A DataFrame showing the ranked results.
    """
    results = []

    # Traverse through the mia-result folder (including sub-folders and construct directory to results)
    for root, _, files in os.walk(mia_result_dir):
        for file in files:
            if file == 'results_summary.csv':
                file_path = os.path.join(root, file)

                # Load the results_summary.csv file
                df = pd.read_csv(file_path, delimiter=';')

                # Filter for the specific brain region and metric
                filtered_df = df[(df['LABEL'] == brain_region) & (df['METRIC'] == metric) & (df['STATISTIC'] == 'MEAN')]

                # If matching rows are found, add them to the results list
                if not filtered_df.empty: # TODO: Here he checks if the df is empty or not.
                    mean_value = filtered_df.iloc[0]['VALUE']
                    # Append tuple
                    results.append({
                        'Path': file_path,
                        'Mean_Value': mean_value # TODO: extend for other information if needed
                    })
                

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Sort results by Mean_Value in descending order
    results_df = results_df.sort_values(by='Mean_Value', ascending=False).reset_index(drop=True)

    # Add a ranking column
    results_df['Rank'] = results_df.index + 1

    # Filter for the requested rank
    ranked_results = results_df[results_df['Rank'] == rank]

    return ranked_results


if __name__ == "__main__":
    # Example usage
    mia_result_dir = "mialab/mia-result/"  # Path to the mia-result folder
    metric = "DICE"  # Evaluation metric (e.g., 'DICE', 'JACRD')
    brain_region = "WhiteMatter"  # Select brain region: WhiteMatter, GreyMatter, Hippocampus, Amygdala, Thalamus
    rank = 1  # Rank to select (e.g., 1 for best, 2 for second best)
    save = True # If true, saved to folder 'ranking' in mia-results, otherwise just printed 

    # Get the ranked results
    ranked_results = find_best_results(mia_result_dir=mia_result_dir, 
                                       metric=metric, 
                                       brain_region=brain_region, 
                                       rank=rank)

    if ranked_results.empty:
        print(f"No results found for metric '{metric}' and brain region '{brain_region}'.")
    else:
        print(f"Top result for '{metric}' in '{brain_region}' (Rank {rank}):")
        print(ranked_results)
        if save:            
                # save to a CSV file
                # create a result directory with timestamp
                t = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                ranked_results.to_csv(f'mialab/mia-result/ranking/{brain_region}_{metric}_{t}.csv', index=False)
                print(f"Results saved to 'mialab/mia-result/ranking/{brain_region}_{metric}_{t}.csv'")
