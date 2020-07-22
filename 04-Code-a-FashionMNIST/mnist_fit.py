import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, datasets

# Prepare the Data (Helper Function)
def prepare_mnist_features_and_labels(x, y):
  x = tf.cast(x, tf.float32) / 255.0
  y = tf.cast(y, tf.int64)
  return x, y

# Download and Define the Dataset
def mnist_dataset():
  (x, y), (x_val, y_val) = datasets.fashion_mnist.load_data()
  print('x/y shape:', x.shape, y.shape)
  y = tf.one_hot(y, depth=10)
  y_val = tf.one_hot(y_val, depth=10)
  ds = tf.data.Dataset.from_tensor_slices((x, y))
  ds = ds.map(prepare_mnist_features_and_labels)
  ds = ds.shuffle(60000).batch(100)

  ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val))
  ds_val = ds_val.map(prepare_mnist_features_and_labels)
  ds_val = ds_val.shuffle(10000).batch(100)

  return ds,ds_val


# Define the Main Function
def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}

    # Get the Dataset
    train_dataset, val_dataset = mnist_dataset()

    # Define the Model
    model = keras.Sequential([
        layers.Reshape(target_shape=(28 * 28,), input_shape=(28, 28)),
        layers.Dense(200, activation='relu'),
        layers.Dense(200, activation='relu'),
        layers.Dense(200, activation='relu'),
        layers.Dense(10)])
    
    # Build the Model
    model.build(input_shape=[None, 28 * 28])

    # Print the Summary of the Model
    model.summary()

    # no need to use compile if you have no loss/optimizer/metrics involved here.
    model.compile(optimizer=optimizers.Adam(0.001),
                  loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Fit the Model
    model.fit(train_dataset.repeat(), epochs=30, steps_per_epoch=500,
              validation_data=val_dataset.repeat(),
              validation_steps=2)


if __name__ == '__main__':
    main()
