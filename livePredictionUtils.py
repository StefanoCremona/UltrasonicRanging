# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:47:57 2020

@author: e7470
"""
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt
import keras
from PIL import Image
import json
#import tensorflow as tf

def loadModel(model_json_file_name, weights_file_name):
    print('Loading model from file: ' + model_json_file_name)
    json_file = open(model_json_file_name, 'r')
    model_json = json_file.read()
    json_file.close()
    mymodel = model_from_json(model_json)
    mymodel.load_weights(weights_file_name)
    return mymodel

def loadClassesNames(file):
    print('Loading classes from file: ' + file)
    classes_file = open(file, 'r')
    classes_json = classes_file.read()
    classes_names = json.loads(classes_json)
    classes_file.close()
    return classes_names

def compileModel(model):
    import tensorflow as tf
    model.compile(optimizer='adam', 
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
                  metrics=['accuracy'])
    return model

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def plot_value_array(predictions_array, class_names):
  plt.grid(False)
  plt.xticks(range(len(class_names)), class_names, rotation='vertical')
  plt.yticks([])
  thisplot = plt.bar(range(len(class_names)), predictions_array, color="gray")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('green')

def getImageToPlot(file):
    img = Image.open(file)
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = np.array(img)
    img = rgb2gray(img)
    return img

def getPredictions(probModel, img):
    images = np.asarray([img])
    images = images / 255.0
    return probModel.predict([images])

def plotImgAndPrediction(img, prediction, class_names):
    plt.figure(figsize=(12,6))
    plt.subplot(1,2,1)
    plt.imshow(img, cmap=plt.cm.binary)
    plt.subplot(1,2,2)
    plot_value_array(prediction, class_names)

def getProbabilityModel(model_file, weights_file):
    model = loadModel(model_file, weights_file)
    compileModel(model)
    return keras.Sequential([model, keras.layers.Softmax()])