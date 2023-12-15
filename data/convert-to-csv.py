# Converts data to a csv file

import pandas as pd
import numpy as np

# load data from npy files
# both are AMOUNTx3x3 arrays
AMOUNT = 100
x_data = np.load('data/x.npy')[:AMOUNT]
y_data = np.load('data/y.npy')[:AMOUNT]

# convert data to dataframes
def create_dataframe(array):
    df = pd.DataFrame(columns=['a', 'b', 'c'])
    for board in array:
        for row in board:
            df.loc[len(df)] = row
        # add EMPTY line betwen boards
        df.loc[len(df)] = ['', '', '']
    return df
x_df = create_dataframe(x_data)
y_df = create_dataframe(y_data)

# save to csv
x_df.to_csv('data/x.csv', index=False, header=False)
y_df.to_csv('data/y.csv', index=False, header=False)