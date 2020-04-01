# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 22:24:47 2020
from https://www.tensorflow.org/tutorials/load_data/images
@author: e7470
"""
import IPython.display as display
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import pathlib
# import keras

data_dir = pathlib.Path("C:/Users/e7470/dataTest/trainRowNormal")
test_dir = pathlib.Path("C:/Users/e7470/dataTest/testRowNormal")
models_dir = pathlib.Path("C:/Users/e7470/models")

CLASS_NAMES = np.array([item.name for item in data_dir.glob('*')])
# CLASS_NAMES = np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])
print('Labels: ' + str(CLASS_NAMES))

image_count = len(list(data_dir.glob('*/*.png')))
print('Total images between training and test:' + str(image_count))

def showSamples():
    samples = list(data_dir.glob(CLASS_NAMES[0] + '/*'))
    
    print("Samples from " + CLASS_NAMES[0])
    for image_path in samples[:3]:
        display.display(Image.open(str(image_path)))
        
    samples = list(data_dir.glob(CLASS_NAMES[1] + '/*'))
    
    print("Samples from " + CLASS_NAMES[1])
    for image_path in samples[:3]:
        display.display(Image.open(str(image_path)))

# showSamples()
# Function to voncert images to gray scale
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
    
# The 1./255 is to convert from uint8 to float32 in range [0,1].
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

BATCH_SIZE = 1000
IMG_HEIGHT = 500
IMG_WIDTH = 500
STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)

train_data_gen = image_generator.flow_from_directory(directory=str(data_dir),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     classes = list(CLASS_NAMES),
                                                     class_mode = 'binary'
                                                     )

test_data_gen = image_generator.flow_from_directory(directory=str(test_dir),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     classes = list(CLASS_NAMES),
                                                     class_mode = 'binary'
                                                     )

# Inspect a batch:
def show_batch(image_batch, label_batch, rangeN):
  plt.figure(figsize=(10,10))
  for n in range(rangeN):
      ax = plt.subplot(5,5,n+1)
      plt.imshow(image_batch[n])
      plt.title(CLASS_NAMES[int(label_batch[n])])
      plt.axis('off')

train_images, train_labels = train_data_gen.next()
test_images, test_labels = test_data_gen.next()

# print(type(train_images))
# print(train_images.shape)
# print(type(train_labels))
# print(train_labels)

# Convert in grayscale np array images. From 28*28*3 to 28*28 vector
train_images = np.asarray([rgb2gray(pi) for pi in train_images])
test_images = np.asarray([rgb2gray(pi) for pi in test_images])

# print(type(train_images))
print('Train images shape: ' + str(train_images.shape))

#print('Train and Test examples:')
show_batch(train_images, train_labels, 25)
show_batch(test_images, test_labels, 5)

# train_labels = keras.utils.to_categorical(train_labels, len(CLASS_NAMES))
# test_labels = keras.utils.to_categorical(test_labels, len(CLASS_NAMES))

