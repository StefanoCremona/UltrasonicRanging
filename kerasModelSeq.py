# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:33:12 2020

@author: e7470
"""
# train_images = train_images / 255.0
# test_images = test_images / 255.0
import keras
import tensorflow as tf
from keras.models import Sequential, model_from_json
from keras.layers import Conv2D, MaxPool2D, Dropout, Dense, Flatten, MaxPooling2D
from datetime import datetime

# run a preprocessing file before
print(train_images.shape)
print(train_labels.shape)

num_classes=len(CLASS_NAMES)
image_h = 500
image_w = 500
image_size = image_h * image_w # 28*28

def fitModel(model):
    model.fit(train_images, train_labels, epochs=10)
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('\nTest loss:', test_loss)
    print('\nTest accuracy:', test_acc)
    return model

def model1():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(image_h, image_w)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy'])
    return model

model = fitModel(model1())
#getDataModel2(train_images, train_labels, test_images, test_labels)
#save the model to json file
model_json = model.to_json()
 
currentDT = datetime.datetime.now() 
currentDTS = currentDT.strftime("%Y%m%d%H%M%S")

with open('model'+currentDTS+'.json', 'w') as json_file:
    json_file.write(model_json)
model.save_weights('mnist_fashion_model'+currentDTS+'.h5')
