import pandas as pd
import os

def split_csv_by_mmsi(input_file):
    # Charge the .csv file in a DataFrame
    df = pd.read_csv(input_file)

    # Group the data by MMSI number
    grouped = df.groupby('sourcemmsi')

    # Create a folder for the splited .csv files
    output_folder = 'csv_by_mmsi'
    os.makedirs(output_folder, exist_ok=True)

    # Save the grouped data in the splited .csv files
    for mmsi, data in grouped:
        output_file = os.path.join(output_folder, f'{mmsi}.csv')
        data.to_csv(output_file, index=False)

    print("Splited .csv file created with success !")

# Call of this function by specifying the path of the .csv file
# input_file_path = 'path/of/your/file.csv'
input_file_path = 'nari_dynamic.csv'
split_csv_by_mmsi(input_file_path)
