# generates all the data for the arrow game
import copy
import os
import random
import numpy as np
import yaml
from board import Board

NUMPOINTS = 100000
DIRECTORY = "data"
FILENAME_X = "x.yaml"
FILENAME_Y = "y.yaml"

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
	board.spin_array(-1 * spin) # spin in reverse
	x_data.append( copy.deepcopy(board.board) )
	y_data.append(spin)
	board.reset()

# write data to file
def write_data(data, path):
	stream = open(path, 'w')
	print("writing to " + path)
	yaml.dump(data, stream)

os.makedirs(DIRECTORY, exist_ok=True)
write_data(x_data, os.path.join(DIRECTORY, FILENAME_X))
write_data(y_data, os.path.join(DIRECTORY, FILENAME_Y))