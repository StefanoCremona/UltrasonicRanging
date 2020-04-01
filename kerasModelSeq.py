# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:33:12 2020

@author: e7470
"""
# train_images = train_images / 255.0
# test_images = test_images / 255.0
import keras
import tensorflow as tf
import numpy as np
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPool2D, Dropout, Dense, Flatten, MaxPooling2D
from datetime import datetime
from os.path import join
import json
import pathlib

epochs = 100
testLabel = 'OneRowNormSeq'+str(epochs) # Give the name to the model file to save
# run a preprocessing file before
print(train_images.shape)
print(train_labels.shape)

models_dir = pathlib.Path("C:/Users/e7470/models")

# to Get this values run kerasPreprocessing
num_classes=len(CLASS_NAMES)
image_h = IMG_HEIGHT
image_w = IMG_WIDTH
image_size = image_h * image_w # eg: 28*28

def fitModel(model):
    model.fit(train_images, train_labels, epochs=epochs)
    return model

def showLossAcc(model):
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('\nTest loss:', test_loss)
    print('\nTest accuracy:', test_acc)

def confModel():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(image_h, image_w)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(num_classes)
    ])
    return model

def compileModel(model):
    model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy'])
    return model

def saveClassesNames(classArray, rootDir, file):
    if str(type(classArray)).rfind("ndarray") >= 0:
        classArray = classArray.tolist()

    classes_json = json.dumps(classArray)
    with open(join(rootDir, file), 'w') as json_file:
        json_file.write(classes_json)
    json_file.close()

model = confModel()
model = compileModel(model)
model = fitModel(model)
showLossAcc(model)

# convert the model to json file
model_json = model.to_json()
 
currentDT = datetime.now()
currentDTS = currentDT.strftime("%Y%m%d%H%M%S")

suffix = currentDTS+testLabel
modelFileName = 'model'+suffix+'.json'
weightsFileName = 'weights'+suffix+'.h5'
classesFileName = "classes"+suffix+".json"

with open(join(models_dir, modelFileName), 'w') as json_file:
    json_file.write(model_json)
model.save_weights(join(models_dir, weightsFileName))
saveClassesNames(CLASS_NAMES, models_dir, classesFileName)

print('Model saved as: ' + modelFileName)
print('Weights saved as: ' + weightsFileName)
print('Classes saved as: ' + classesFileName)
