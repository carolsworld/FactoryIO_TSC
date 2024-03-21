import requests
import csv
from datetime import datetime
import time
import threading

# Global variables
previous_conveyor_speed = None
continue_data_collection = True
trigger_point = 1  # Modify this parameter to match the simulation. 1 for 'sensor', 2 for 'actuator (forced)'
simulation_param = "s_1.39" # Modify this parameter to match the simulation and create file name
row_sequence_number = 0
speed_change_history = []
FACTORY_IO_API_URL = 'http://localhost:7410/api/tags'
FETCH_INTERVAL = 0.5  # Time interval to fetch data in seconds
SIGNIFICANT_CHANGE_THRESHOLD = 1  # A subjective threshold for indicating the magnitude of change, i.e. 1 refers to increase or decrease of speed by 1.

# List of tags to fetch from Factory IO
TAG_NAMES = ['FACTORY I/O (Running)', 'Start', 'I_Check Quality Sensor', 'I_Counter Sensor 1', 'Reset',\
            'Pusher 0 (Front Limit)', 'Pusher 0 (Back Limit)', 'Emergency Stop', 'Potentiometer 0 (V)',\
            'Q_Start Button 1 (Light)', 'Q_Emit boxes', 'Pusher 0', 'Q_Stack Light Green', \
            'Q_Stack Light Yellow', 'Q_Stack Light Red', 'Q_Reset Button 0 (Light)', 'Alarm Siren 0', \
            'Q_Move Conveyor', 'Speed Display', 'Number of Qualified Goods'] 

# Function to stop data collection
def stop_data_collection():
    global continue_data_collection
    continue_data_collection = False
    print("Automatically stopping the data collection.")

# Fetch data from Factory IO
def fetch_data():
    """Fetch data from Factory IO."""
    try:
        response = requests.get(FACTORY_IO_API_URL)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        return response.json()  # Assumes the API returns JSON
    except requests.RequestException as e:
        print(f"Error fetching data from Factory IO: {e}")
        return None

# Assess if the behavior is abnormal based on the frequency of significant changes.
# Within 15 seconds, 5 abnomal changes are detected, the behavior is regarded as abnormal.
def is_abnormal_behavior(recent_changes, time_frame=15, threshold=5):
    current_time = datetime.now().timestamp()
    recent_changes_within_frame = [change for change in recent_changes if current_time - change <= time_frame]
    return len(recent_changes_within_frame) >= threshold

def format_and_append_data_to_csv(data, simulation_param):
    global previous_conveyor_speed, row_sequence_number
    csv_file = f"factory_io_data_{simulation_param}.csv"
    formatted_data = format_data_for_csv(data)
    append_to_csv(formatted_data, csv_file)
    row_sequence_number += 1

def format_data_for_csv(data):
    global previous_conveyor_speed, speed_change_history
    formatted_data = {'Trigger Point': trigger_point}
    conveyor_speed = None
    
    for item in data:
        tag_name = item['name']
        value = item['value']

        # Add the trigger point to the formatted data
        formatted_data['Trigger Point'] = trigger_point

        if tag_name == 'Q_Move Conveyor':
            # Convert the conveyor speed value to float and round it
            try:
                conveyor_speed = round(float(value), 2)
                formatted_data[tag_name] = conveyor_speed
            except ValueError:
                print(f"Error converting Q_Move Conveyor value to float: {value}")
                continue  # In case of conversion failure, skip further processing for this tag
        
        elif tag_name == 'Potentiometer 0 (V)':
            # Round the Potentiometer value to two decimal places
            try:
                potentiometer_value = round(float(value), 2)
                formatted_data[tag_name] = potentiometer_value
            except ValueError:
                print(f"Error converting Potentiometer value to float: {value}")
                continue  # In case of conversion failure, skip further processing for this tag
        
        # For boolean values, convert to integer
        elif isinstance(value, bool):
            formatted_data[tag_name] = int(value)
        else:
            formatted_data[tag_name] = value

    if conveyor_speed is not None:
        # Calculate speed change and round it immediately to prevent floating-point arithmetic issues
        speed_change = round(conveyor_speed - (previous_conveyor_speed if previous_conveyor_speed is not None else 0), 2)
        formatted_data['Speed Change'] = round(speed_change, 2)  # Explicit rounding to 2 decimal places

        # Update speed_change_history
        if abs(speed_change) >= SIGNIFICANT_CHANGE_THRESHOLD:
            speed_change_history.append(datetime.now().timestamp())

        # Acceleration/Deceleration Indicator and return numerical categories
        if is_abnormal_behavior(speed_change_history):
            acc_dec_indicator = 4  # Abnormal behaviour 
        elif speed_change > 0:
            acc_dec_indicator = 2  # Acceleration
        elif speed_change < 0:
            acc_dec_indicator = 3  # Deceleration
        else:
            acc_dec_indicator = 1  # Constant
        formatted_data['Acceleration Indicator'] = acc_dec_indicator
        
        previous_conveyor_speed = conveyor_speed  # Update the previous speed for next iteration

    formatted_data['Trigger Point'] = trigger_point
    formatted_data['Actual Conveyor Status'] = categorize_speed(conveyor_speed if conveyor_speed is not None else 0)
   
    # Resetting conveyor speed change calculations for new simulation
    if not continue_data_collection:
        previous_conveyor_speed = None
    
    return formatted_data


# Categorize conveyor speed by Q_Move Conveyor tag value and return numerical categories
def categorize_speed(speed):
    if -5 < speed < 0:
        return 5  # 'conveyor wrong direction'
    elif speed == 0:
        return 4  # 'conveyor stop'
    elif 0 < speed <= 2.30:
        return 3  # 'conveyor too slow'
    elif 2.31 < speed <= 5.00:
        return 1  # 'normal conveying speed'
    elif 5.01 < speed <= 7.00:
        return 2  # 'conveyor too fast'
    else:
        return 6  # 'abnormal'

# Append the data to a CSV file in the correct format   
def append_to_csv(data, filename):
    global row_sequence_number
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = [
            'Timestamp',
            'Sequence',
            'Trigger Point',
            'I_Check Quality Sensor',
            'I_Counter Sensor 1',
            'Q_Stack Light Green',
            'Q_Stack Light Yellow', 
            'Q_Stack Light Red',
            'Pusher 0 (Front Limit)',
            'Pusher 0 (Back Limit)',
            'Pusher 0',
            'Potentiometer 0 (V)',
            'Q_Move Conveyor',
            'Speed Display',
            'Speed Change',
            'Number of Qualified Goods',
            'Alarm Siren 0',
            'Acceleration Indicator',
            'Actual Conveyor Status',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Filter data dict to contain only keys that are in fieldnames
        filtered_data = {key: data[key] for key in fieldnames if key in data}

        # Ensure sequence number and timestamp are correctly added
        filtered_data['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        filtered_data['Sequence'] = row_sequence_number

        writer.writerow(filtered_data)

def main(simulation_param):
    global continue_data_collection, row_sequence_number, previous_conveyor_speed, speed_change_history
    csv_file = f"factory_io_data_{simulation_param}.csv"
    timer = threading.Timer(60, stop_data_collection)  # Set timer for automatic stopping
    timer.start()
    
    # Ensure the CSV header is written at the beginning of each simulation
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Sequence', 'Trigger Point', 'I_Check Quality Sensor', 'I_Counter Sensor 1',
                      'Q_Stack Light Green', 'Q_Stack Light Yellow', 'Q_Stack Light Red', 'Pusher 0 (Front Limit)',
                      'Pusher 0 (Back Limit)', 'Pusher 0', 'Potentiometer 0 (V)', 'Q_Move Conveyor', 'Speed Display',
                      'Speed Change', 'Number of Qualified Goods', 'Alarm Siren 0', 'Acceleration Indicator',
                      'Actual Conveyor Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # Clear the speed_change_history at the start of each simulation
    speed_change_history = []

    while continue_data_collection:
        data = fetch_data()
        if data:
            formatted_data = format_data_for_csv(data)
            append_to_csv(formatted_data, csv_file)
            row_sequence_number += 1  # Increment sequence for each data entry
        time.sleep(FETCH_INTERVAL)

    # Reset variables for potential future use
    continue_data_collection = True
    row_sequence_number = 0
    previous_conveyor_speed = None

if __name__ == "__main__":
    main(simulation_param)