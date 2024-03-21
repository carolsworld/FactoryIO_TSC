import pandas as pd
import os

# Define your base directory where the folders are located
base_dir = 'C:/Users/babya/Documents/Project/Datasets'
output_file_path = 'C:/Users/babya/Documents/Project/combined_dataset.csv'

# Initialize a list to hold all DataFrames
dfs = []

# Initialize a counter for file numbering
file_number = 1

for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                # Add the folder name as the category
                df['Category'] = folder_name
                # Add the file number
                df['FileNumber'] = file_number
                dfs.append(df)
                file_number += 1  # Increment the file number

# Combine all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_file_path, index=False)

print(f"Combined dataset saved to {output_file_path}")