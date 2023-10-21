
# represents a board of arrows
class Board:
	# dimensions is a tuple of (width, height)
	def __init__(self, dimensions):
		self.dimensions = dimensions
		self.board = [] # [row1, row2, row3, ...]
		for y in range(dimensions[0]):
			self.board.append([])
			for x in range(dimensions[1]):
				self.board[y].append(0)
	
	# spin the arrow at the given location
	def spin(self, location, direction):
		[x, y] = location
		self.board[y][x] += direction
	# takes in an array the same size as the board and spins the arrows
	def spin_array(self, array):
		for y in range(self.dimensions[0]):
			for x in range(self.dimensions[1]):
				self.spin([x, y], array[y][x])
	
	def reset(self):
		for y in range(self.dimensions[0]):
			for x in range(self.dimensions[1]):
				self.board[y][x] = 0