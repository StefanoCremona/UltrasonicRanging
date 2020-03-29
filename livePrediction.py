# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:47:57 2020

@author: e7470
"""

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import tensorflow as tf
from keras.models import model_from_json
from os.path import join
import pathlib
import matplotlib.pyplot as plt
import PIL
import keras
from PIL import Image
import json


models_dir = pathlib.Path("C:/Users/e7470/models")
test_dir = pathlib.Path("C:/Users/e7470/dataTest/test/oneNormT1")
data_dir = pathlib.Path("C:/Users/e7470/dataTest/train")

def loadModel(modelName, weightName):
    json_file_name =modelName
    print('Loading model from file: ' + json_file_name)
    json_file = open(join(models_dir, json_file_name), 'r')
    model_json = json_file.read()
    json_file.close()
    mymodel = model_from_json(model_json)
    mymodel.load_weights(join(models_dir, weightName))
    return mymodel

def loadClassesNames(rootDir, file):
    print('Loading classes from file: ' + file)
    classes_file = open(join(rootDir, file), 'r')
    classes_json = classes_file.read()
    classes_names = json.loads(classes_json)
    classes_file.close()
    return classes_names

def compileModel(model):
    model.compile(optimizer='adam', 
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
                  metrics=['accuracy'])
    return model

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def plot_value_array(predictions_array):
  plt.grid(False)
  plt.xticks(range(len(CLASS_NAMES)), CLASS_NAMES, rotation='vertical')
  plt.yticks([])
  thisplot = plt.bar(range(len(CLASS_NAMES)), predictions_array, color="gray")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('green')

prefix = "Seq20200324222341AllFilled"
CLASS_NAMES = loadClassesNames(models_dir, "classesNames"+prefix+".json")
model = loadModel('model'+prefix+'.json', 'weights'+prefix+'.h5')

compileModel(model)

img_path = '202003101656127128Tsquared1.png'
img = Image.open(join(test_dir, img_path))
img = img.resize((300, 300), PIL.Image.ANTIALIAS)
img = np.array(img)
img=rgb2gray(img)

# img = np.reshape(img, (1, 300, 300))
probability_model = keras.Sequential([model, keras.layers.Softmax()])
images = np.asarray([img])
images = images / 255.0
predictions = probability_model.predict([images])
# print(predictions[0]) # 'numpy.ndarray', 300*300
# print(np.argmax(predictions))

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.imshow(img, cmap=plt.cm.binary)
plt.subplot(1,2,2)
plot_value_array(predictions[0])
