###############################
## Zachary Hoffman
## Assignment 1
## January 27, 2021
## MNIST Written Number Identifier

# Import libaries
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

# Grab MNIST data from keras libraries
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path="mnist.npz")

# Set all values between 0 and 1
train_images, test_images = train_images / 255, test_images / 255

# All possible output outcomes, correspond to an output node
class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Create basic model
model = models.Sequential()

# Layer 1 - CNN - input shape: [28, 28, 1] - feature map of 3x3, 28 nodes
model.add(layers.Conv2D(28, (3, 3), activation="relu", input_shape=(28, 28, 1), batch_size=32))
# Layer 2 - Pools the feature maps using max to 2x2
model.add(layers.MaxPooling2D((2, 2)))
# Layer 3 - CNN - 56 input nodes, 3x3 feature map
model.add(layers.Conv2D(56, (3, 3), activation="relu"))
# Layer 4 - Pools the feature maps using max to 2x2
model.add(layers.MaxPooling2D((2, 2)))
# Layer 5 - CNN - 56 input nodes, 3x3 feature map
model.add(layers.Conv2D(56, (3, 3), activation="relu"))
# Layer 6 - Flattens matrices
model.add(layers.Flatten())
# Layer 7 - Dense layer
model.add(layers.Dense(56, activation="tanh"))
# Layer 8 - outputs 10 nodes, the possible digits
model.add(layers.Dense(10))

model.compile(
    optimizer="adam",   # Use gradient descent as backpropagation algorithm
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"]
)

# Duplicate training and testing data
train_init_img, test_init_img = train_images, test_images

# Expand dimensions so the data will correcly fit the model
train_images = tf.expand_dims(train_images, axis=-1)
test_images = tf.expand_dims(test_images, axis=-1)

# Train model using 1 epoch
history = model.fit(train_images, train_labels, epochs=1, validation_data=(test_images, test_labels))

# Get loss and accuracy data
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

# Allows user to select an example to test
while True:
    index = input("Enter a number between 200 and 0 for the prediction index\n>")
    # Checks if input is a valid number
    if index.isnumeric():
        if int(index) <= 200:
            prediction_index = int(index)

            # Predicts using the model
            predictions = model.predict(test_images)

            # Show result image
            plt.figure()
            plt.imshow(test_init_img[prediction_index], cmap=plt.cm.binary)
            plt.colorbar()
            plt.grid(False)
            plt.show()

            # Show result prediction
            print("prediction:", class_names[np.argmax(predictions[prediction_index])])
