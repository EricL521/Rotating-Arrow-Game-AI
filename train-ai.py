import os
from matplotlib import pyplot as plt
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras
from keras_core import ops

# ===== load data config =====
DATA_DIRECTORY = "data"
config = yaml.load(open( os.path.join(DATA_DIRECTORY, "config.yaml") , "r"), Loader=yaml.Loader)

FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# ===== load data =====

# Increase training data size if model plateaus <=======================================================
# Decrease batch size first, though, see below
# NOTE: if you notice a difference between val_loss and loss,
# increase this number
# I started it at ~10000
TRAINING_DATA_SIZE = 100000

print("Loading data")
x_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_X))[:TRAINING_DATA_SIZE]
y_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_Y))[:TRAINING_DATA_SIZE]
print("x_train.shape:", x_train.shape)
print("y_train.shape:", y_train.shape)

# ===== create/load model =====
def custom_accuracy(y_true, y_pred):
	# round y_pred and calculate proportion of correct predictions
	return ops.equal(ops.round(y_pred), y_true).mean()

MODEL_DIRECTORY = "model"
if os.path.exists(os.path.join(MODEL_DIRECTORY, "model.keras")):
	print("Loading model")
	model = keras.models.load_model(
		os.path.join(MODEL_DIRECTORY, "model.keras"), 
		custom_objects={"custom_accuracy": custom_accuracy}
	)
	# the learning rate is relatively high, so it can get out of local minima
	# it is decreased during runtime by a callback
	learning_rate = 0.05
else:
	print("Creating model")
	model = keras.Sequential([
		keras.layers.Input(shape=(3, 3)),
		keras.layers.Flatten(),
		keras.layers.Dense(243, activation='leaky_relu'),
		keras.layers.Dense(27, activation='leaky_relu'),
		keras.layers.Dense(9, activation='leaky_relu'),
		keras.layers.Reshape((3, 3)),
	])
	learning_rate = 0.1

# ===== compile model =====
model.compile(
	optimizer=keras.optimizers.SGD(learning_rate=learning_rate), 
	loss=keras.losses.MeanSquaredError(), 
	metrics=[custom_accuracy]
)

model.summary()
model.evaluate(x_train, y_train, verbose=2)

# ===== backup model before training =====
print("Backing up model")
# if folder doesn't exist, create it
if not os.path.exists(MODEL_DIRECTORY):
	os.makedirs(MODEL_DIRECTORY)
model.save(os.path.join(MODEL_DIRECTORY, "old-model.keras"))

# ===== train model =====
callbacks = [
    keras.callbacks.ModelCheckpoint(filepath=os.path.join(MODEL_DIRECTORY, "model_at_epoch_{epoch}.keras")),
	keras.callbacks.ModelCheckpoint(filepath=os.path.join(MODEL_DIRECTORY, "best_model.keras"), save_best_only=True, verbose=1),
	keras.callbacks.ReduceLROnPlateau(patience=20, factor=0.5, min_lr=0.000001, verbose=1),
    keras.callbacks.EarlyStopping(patience=100, min_delta=0.0001),
]

# halve batch_size if model loss starts <=======================================================
# plateauing even after multiple starts of the program
# once it gets decently small, increase 
# training data size and batch size 
# ex. I increased training size to 50000 and batch size to 128
# I started it at ~32
batch_size = 32
epochs = 10000
history = model.fit(
	x_train, y_train,
	validation_split=0.2,
	batch_size=batch_size, 
	epochs=epochs,
	callbacks=callbacks
)

# ===== save model =====
print("Saving model")
model.save(os.path.join(MODEL_DIRECTORY, "model.keras"))


# ===== display results =====
history_dict = history.history

acc = history_dict['mean_metric_wrapper']
val_acc = history_dict['val_mean_metric_wrapper']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

plt.title('Training & validation loss & accuracy')
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.plot(epochs, acc, 'og', label='Training acc')
plt.plot(epochs, val_acc, 'g', label='Validation acc')
plt.xlabel('Epochs')
plt.ylabel('Loss/Accuracy')

plt.legend()

plt.show()
