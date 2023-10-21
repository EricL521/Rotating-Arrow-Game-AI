import os
from matplotlib import pyplot as plt
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras

# load data config
DATA_DIRECTORY = "data"
config = yaml.load(open( os.path.join(DATA_DIRECTORY, "config.yaml") , "r"), Loader=yaml.Loader)

FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# load data
print("Loading data")
x_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_X))
y_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_Y))
# process data
print("x_train.shape:", x_train.shape)
print("y_train.shape:", y_train.shape)

# create/load model
MODEL_DIRECTORY = "model"
if os.path.exists(os.path.join(MODEL_DIRECTORY, "model.keras")):
	print("Loading model")
	model = keras.models.load_model(os.path.join(MODEL_DIRECTORY, "model.keras"))
else:
	print("Creating model")
	model = keras.Sequential([
		keras.layers.Input(shape=(4, 4)),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(16, activation="relu"),
		keras.layers.Reshape((4, 4)),
	])

model.summary()

model.compile(
	optimizer=keras.optimizers.SGD(momentum=0.8, learning_rate=0.02), 
	loss=keras.losses.MeanSquaredError(), 
	metrics=["accuracy"]
)

# train model
callbacks = [
    keras.callbacks.ModelCheckpoint(filepath=os.path.join(MODEL_DIRECTORY, "model_at_epoch_{epoch}.keras")),
    keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=20),
]

batch_size = 20
epochs = 1000
history = model.fit(
	x_train, y_train,
	validation_split=0.2,
	batch_size=batch_size, 
	epochs=epochs,
	callbacks=callbacks
)

# save model
model.save(os.path.join(MODEL_DIRECTORY, "model.keras"))


# show results
history_dict = history.history

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
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
