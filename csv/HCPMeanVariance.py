import pandas as pd


def processDataFrame(df):
    # Sort the DataFrame by 'subject' in ascending order
    df.sort_values('subject', inplace=True)
    #Drop NG Sim column
    df.drop('NG sim', axis=1, inplace=True)
    # Group the DataFrame by 'subject'
    grouped_df = df.groupby('subject')

    print(grouped_df.groups)

   # Compute the mean and variance for each SC column per subject
    mean_values = grouped_df.mean()
    var_values = grouped_df.var()

   # Rename the columns to include the 'mean' and 'var' prefixes
    mean_columns = {col: f'{col}_mean' for col in mean_values.columns}
    var_columns = {col: f'{col}_var' for col in var_values.columns}
    mean_values.rename(columns=mean_columns, inplace=True)
    var_values.rename(columns=var_columns, inplace=True)

    # Merge the mean and variance DataFrames into a single DataFrame
    processed_df = pd.concat([mean_values, var_values], axis=1)

    # Assign the correct subject to the DataFrame
    processed_df['subject'] = processed_df.index


    # # # Remove the 'NG Sim' column
    # processed_df.drop('NG sim', axis=1, inplace=True)

    # Reset the index of the DataFrame
    df.reset_index(inplace=True, drop=True)

    # # Load the subject name from subjects.txt and add them to the DataFrame
    # subjects = pd.read_csv('subjects.txt', header=None)
    # df['Subject'] = subjects

    #Make the subjects the first column
    # cols = df.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    # processed_df = df[cols]

    return processed_df

# Specify the file path to the CSV
file_path = 'output/convergenceHCP_20percent.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, index_col="Unnamed: 0")

print(df)

df = processDataFrame(df)

print(df)

# Assuming your DataFrame is named df
output_file_path = 'output/convergenceHCP_20percent_mean_variance.csv'

# Export the DataFrame to a CSV file
df.to_csv(output_file_path, index=False)

