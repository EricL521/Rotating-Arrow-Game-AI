import numpy as np
import yaml
import os

# load config file
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
config_file = open(os.path.join(DIRECTORY, "config.yaml"), "r")
config = yaml.load(config_file, Loader=yaml.Loader)

FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# Load the data
x_train = np.load(os.path.join(DIRECTORY, FILENAME_X))
y_train = np.load(os.path.join(DIRECTORY, FILENAME_Y))

# print data
print("X_train: ")
print(x_train)
print("Y_train: ")
print(y_train)