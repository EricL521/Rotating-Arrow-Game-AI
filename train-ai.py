import os
from matplotlib import pyplot as plt
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras
from keras_core import ops

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
	learning_rate = 0.05
else:
	print("Creating model")
	model = keras.Sequential([
		keras.layers.Input(shape=(4, 4)),
		keras.layers.Rescaling(scale=1.0/4.0),
		keras.layers.Flatten(),
		keras.layers.Dense(512, activation="relu"),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(16, activation="relu"),
		keras.layers.Reshape((4, 4)),
		keras.layers.Rescaling(scale=4.0),
	])
	learning_rate = 0.1
	
model.compile(
	optimizer=keras.optimizers.SGD(learning_rate=learning_rate), 
	loss=keras.losses.MeanSquaredError(), 
	metrics=[custom_accuracy]
)

model.summary()
model.evaluate(x_train, y_train, verbose=2)

# train model
callbacks = [
    keras.callbacks.ModelCheckpoint(filepath=os.path.join(MODEL_DIRECTORY, "model_at_epoch_{epoch}.keras")),
	keras.callbacks.ReduceLROnPlateau(patience=10, factor=0.5, min_lr=0.000001, verbose=1),
    keras.callbacks.EarlyStopping(patience=100),
]

batch_size = 1024
epochs = 10000
history = model.fit(
	x_train, y_train,
	validation_split=0.2,
	batch_size=batch_size, 
	epochs=epochs,
	callbacks=callbacks
)

# save model
print("Saving model")
model.save(os.path.join(MODEL_DIRECTORY, "model.keras"))


# show results
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
