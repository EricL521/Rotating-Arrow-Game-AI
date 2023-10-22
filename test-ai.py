import os
import numpy as np
import tkinter
from UIBoard import UIBoard

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras
from keras_core import ops

# ===== load model =====
MODEL_PATH = "model.keras"
def custom_accuracy(y_true, y_pred):
	# round y_pred and calculate proportion of correct predictions
	return ops.equal(ops.round(y_pred), y_true).mean()
model = keras.models.load_model(MODEL_PATH, custom_objects={"custom_accuracy": custom_accuracy})
print("model loaded")

def update_solution(*_):
	board = np.array(click_board.board)
	board = np.expand_dims(board, 0)
	# predict
	prediction = model.predict(board)[0]
	# update UI
	solution_board.set_board(np.round(prediction).astype(int))

# ===== create UI =====
root = tkinter.Tk()
root.title("Arrow AI")

BOARD_SIZE = 300
root.geometry(f"{(10+BOARD_SIZE)*2}x{BOARD_SIZE + 200}")
root.minsize(((10+BOARD_SIZE)*2), BOARD_SIZE + 200)

# ===== create Bottom Frame =====
bottom_frame = tkinter.Frame(root, width=BOARD_SIZE*2, height=200)
bottom_frame.pack(side=tkinter.BOTTOM)

# ===== create solved label =====
solved_label = tkinter.Label(bottom_frame, text="Solved!", font=("Helvetica", 20), pady=10)
solved_label.pack(side=tkinter.TOP)
def update_solved_label(*_):
	if click_board.is_solved():
		solved_label.config(text="Solved!")
	else:
		solved_label.config(text="Unsolved")

# ===== create buttons =====
def reset():
	click_board.reset()
	solution_board.reset()
	update_solution()
	update_solved_label()
reset_button = tkinter.Button(bottom_frame, text="Reset", font=("Helvetica", 20), padx=10, pady=10, command=reset)
reset_button.pack(side=tkinter.LEFT)

def scramble():
	click_board.spin_array(np.random.randint(0, 4, (4, 4)))
	update_solution()
	update_solved_label()
scramble_button = tkinter.Button(bottom_frame, text="Scramble", font=("Helvetica", 20), padx=10, pady=10, command=scramble)
scramble_button.pack(side=tkinter.LEFT)

# ===== create boards =====
def create_board_frame(root, title, board_size, side):
	frame = tkinter.Frame(root, width=1, height=1, borderwidth=10)
	frame.pack(side=side, fill='both', expand=True)
	frame.columnconfigure(0, weight=1)
	frame.rowconfigure(1, weight=1)
	label = tkinter.Label(frame, text=title, font=("Helvetica", 20))
	label.grid(row=0, column=0)
	board_frame = tkinter.Frame(frame, width=board_size, height=board_size,
							 highlightbackground="black", highlightcolor="black", highlightthickness=1)
	board_frame.grid(row=1, column=0, sticky="nesw")
	return frame, board_frame

top_frame = tkinter.Frame(root, width=1, height=1, pady=10)
top_frame.pack(side=tkinter.TOP, fill='both', expand=True)

left_frame, left_board_frame = create_board_frame(top_frame, "Puzzle (click to spin)", BOARD_SIZE, tkinter.LEFT)
click_board = UIBoard([4, 4], left_board_frame, BOARD_SIZE, view_only=False, 
							on_click=[update_solution, update_solved_label])

right_frame, right_board_frame = create_board_frame(top_frame, "Solution (click to apply)", BOARD_SIZE, tkinter.RIGHT)
def apply_solution(location, value):
	if value != 0:
		click_board.spin(location, value)
		update_solution()
		update_solved_label()
solution_board = UIBoard([4, 4], right_board_frame, BOARD_SIZE, display_strings=["0", "1", "2", "3"], view_only=True,
								on_click=[apply_solution, update_solved_label])

# ===== update solution =====
update_solution()

# ===== start the event loop =====
root.mainloop()
