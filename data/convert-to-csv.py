# Converts data to a csv file

import pandas as pd
import numpy as np
import yaml
import os

# load config.yaml
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
config_file = open(os.path.join(DIRECTORY, "config.yaml"), "r")
config = yaml.load(config_file, Loader=yaml.Loader)
FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# load data from npy files
# both are AMOUNTx3x3 arrays
AMOUNT = 100
x_data = np.load(os.path.join(DIRECTORY, FILENAME_X))[:AMOUNT]
y_data = np.load(os.path.join(DIRECTORY, FILENAME_Y))[:AMOUNT]

# convert data to dataframes
def create_dataframe(array):
    # create columns depending on size of array
    row_size = len(array[0][0])
    columns = ['c' + str(i) for i in range(row_size)]
    df = pd.DataFrame(columns=columns)
    for board in array:
        for row in board:
            df.loc[len(df)] = row
        # add EMPTY line betwen boards
        df.loc[len(df)] = ['' for i in range(row_size)]
    return df
x_df = create_dataframe(x_data)
y_df = create_dataframe(y_data)

# save to csv
x_df.to_csv(os.path.join(DIRECTORY, FILENAME_X.replace('.npy', '.csv')), index=False, header=False)
y_df.to_csv(os.path.join(DIRECTORY, FILENAME_Y.replace('.npy', '.csv')), index=False, header=False)