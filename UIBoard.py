import sys
sys.path.append('data')
from board import Board
import tkinter

class UIBoard(Board):
	def __init__(self, dimensions, root, board_size, display_strings=["↑", "→", "↓", "←"], view_only=False, on_click=[]):
		super(UIBoard, self).__init__(dimensions)
		self.root = root
		self.initialize_root()

		self.board_size = board_size
		self.arrows = display_strings
		self.view_only = view_only
		self.on_click_funcs = on_click

		# generate board
		self.create_board()

	def initialize_root(self):
		self.root.grid_propagate(False)
		self.root.columnconfigure(tuple(range(self.dimensions[0])), weight=1)
		self.root.rowconfigure(tuple(range(self.dimensions[1])), weight=1)
	def create_board(self):
		FONT_SIZE = self.board_size // self.dimensions[0] // 2
		self.tkBoard = []
		for y in range(self.dimensions[0]):
			self.tkBoard.append([])
			for x in range(self.dimensions[1]):
				self.tkBoard[y].append( tkinter.Button(
					self.root, 
					width=self.board_size // self.dimensions[0],
					height=self.board_size // self.dimensions[1],
					text="", font=("Helvetica", FONT_SIZE),
					command=lambda location=[x, y]: self.on_click(location)
				))
				self.tkBoard[y][x].grid(row=y, column=x, sticky="nesw")
		self.update_UI()
	def on_click(self, location):
		if not self.view_only:
			self.spin(location, 1)
			self.update_UI()

		for func in self.on_click_funcs:
			func(location, self.board[location[1]][location[0]])

	# updates UI to match board
	def update_UI(self):
		for y in range(self.dimensions[0]):
			for x in range(self.dimensions[1]):
				self.tkBoard[y][x].configure(text=self.arrows[self.board[y][x]])

	def spin(self, location, direction):
		super(UIBoard, self).spin(location, direction)
		self.update_UI()
	def spin_array(self, array):
		super().spin_array(array)
		self.update_UI()

	def set_board(self, board):
		super().set_board(board)
		self.update_UI()
	def reset(self):
		super().reset()
		self.update_UI()


