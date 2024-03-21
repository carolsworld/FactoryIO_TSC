import pandas as pd

# Load the combined dataset
file_path = 'C:/Users/babya/Documents/Project/combined_dataset.csv'
df = pd.read_csv(file_path)

# Specify the columns you want to keep
columns_of_interest = ['FileNumber','Sequence','Timestamp', 'Potentiometer 0 (V)', 'Q_Move Conveyor',
                       'Speed Display', 'Speed Change', 'Acceleration Indicator', 
                       'Actual Conveyor Status', 'Category']

# Filter the dataframe to keep only the specified columns
filtered_df = df[columns_of_interest]

df = pd.DataFrame({
    'Category': [
        'Sensors_NormalSpeed', 'Sensors_TooSlowOrStop', 'Sensors_Oscillate', 
        'Sensors_WrongDirection', 'ForcedActuator_Normal', 'ForcedActuator_TooSlowOrStop', 
        'ForcedActuator_TooFast', 'ForcedActuator_ExtremelyFast', 'ForcedActuator_Oscillate', 
        'ForcedActuator_WrongDirection'
    ]
})

# Mapping of categories to numeric values
category_mapping = {
    'Sensors_NormalSpeed': 1,
    'Sensors_TooSlowOrStop': 2,
    'Sensors_Oscillate': 3,
    'Sensors_WrongDirection': 4,
    'ForcedActuator_Normal': 5,
    'ForcedActuator_TooSlowOrStop': 6,
    'ForcedActuator_TooFast': 7,
    'ForcedActuator_ExtremelyFast': 8,
    'ForcedActuator_Oscillate': 9,
    'ForcedActuator_WrongDirection': 10
}

# Apply mapping
filtered_df['CategoryRef'] = filtered_df['Category'].replace(category_mapping)
filtered_df = filtered_df.drop(columns=['Category'])

# Save the filtered dataset to a new CSV file
filtered_file_path = 'C:/Users/babya/Documents/Project/filtered_dataset.csv'
filtered_df.to_csv(filtered_file_path, index=False)

print(f"Filtered dataset saved to {filtered_file_path}")
