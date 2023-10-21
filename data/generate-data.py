# generates all the data for the arrow game
import copy
import os
import random
import numpy as np
import yaml
from board import Board

# load config
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

config_file = open(os.path.join(DIRECTORY, "config.yaml"), "r")
config = yaml.load(config_file, Loader=yaml.Loader)

NUMPOINTS = config["num_points"]
FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# generates a randomized array of dim[x, y]
def get_random_array(dim):
	array = []
	for y in range(dim[1]):
		array.append([])
		for x in range(dim[0]):
			array[y].append(random.randint(0, 3))
	return np.array(array)

# create a board and array for storing data
board = Board([4, 4])
x_data = []
y_data = []
for i in range(NUMPOINTS):
	print(i)
	spin = get_random_array(board.dimensions)
	board.spin_array(-1 * spin) # spin in reverse, so that the array is the solution
	x_data.append( copy.deepcopy(board.board) )
	y_data.append(spin)
	board.reset()

# write data to file
os.makedirs(DIRECTORY, exist_ok=True)
np.save(os.path.join(DIRECTORY, FILENAME_X), x_data)
np.save(os.path.join(DIRECTORY, FILENAME_Y), y_data)