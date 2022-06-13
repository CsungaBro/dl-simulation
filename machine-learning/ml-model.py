import tensorflow as tf
from tensorflow.keras import layers, Input

image_size = (36, 36, 1)

model = tf.keras.models.Sequential([
  Input(image_size),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(16, activation='relu'),
  layers.Reshape((4, 4, 1)),
  layers.UpSampling2D(),
#   layers.Conv2DTranspose(64, 3, padding='same', activation='relu'),
#   layers.UpSampling2D(),
  layers.Conv2DTranspose(32, 3, padding='same', activation='relu'),
  layers.UpSampling2D(),
  layers.Conv2DTranspose(16, 3, padding='same', activation='relu'),
  layers.Conv2DTranspose(1, 3, padding='same', activation='relu'),

])

model.build()

model.summary()