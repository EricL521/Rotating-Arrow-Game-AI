
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
	
	# simulates a click at location, spins all arrows around it, and itself
	def spin(self, location, direction):
		[x, y] = location
		for i in range(-1, 2):
			for j in range(-1, 2):
				if x + i < 0 or x + i >= self.dimensions[0] or y + j < 0 or y + j >= self.dimensions[1]:
					continue # don't spin out of bounds
				self.board[y + j][x + i] += direction
				self.board[y + j][x + i] %= 4
	# takes in an array the same size as the board and spins the arrows
	def spin_array(self, array):
		for y in range(self.dimensions[0]):
			for x in range(self.dimensions[1]):
				self.spin([x, y], array[y][x])
	
	def reset(self):
		for y in range(self.dimensions[0]):
			for x in range(self.dimensions[1]):
				self.board[y][x] = 0