# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:43:54 2020

@author: e7470
"""
import matplotlib.pyplot as plt
import keras
import tensorflow as tf
from keras.models import model_from_json
import pathlib
import numpy as np
from os.path import join
from livePredictionUtils import getProbabilityModel, loadClassesNames, getPredictions, plotImgAndPrediction

data_dir = pathlib.Path("C:/Users/e7470/dataTest/00_train")
test_dir = pathlib.Path("C:/Users/e7470/dataTest/01_test")
models_dir = pathlib.Path("C:/Users/e7470/models")
# Type here the testName of the model you want to load
modelName = "20200402150758OneNormLatSeq100" # "20200401150306AllFilledSeq100"

CLASS_NAMES = np.array([item.name for item in data_dir.glob('*')])

BATCH_SIZE = 1000
IMG_HEIGHT = 300
IMG_WIDTH = 300

# showSamples()
# Function to voncert images to gray scale
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

CLASS_NAMES = loadClassesNames(join(str(models_dir), 'classes'+modelName+'.json'))

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_data_gen = image_generator.flow_from_directory(directory=str(test_dir),
                                                     batch_size=BATCH_SIZE,
                                                     shuffle=True,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     classes = list(CLASS_NAMES),
                                                     class_mode = 'binary'
                                                     )

test_images, test_labels = test_data_gen.next()

# print(type(train_images))
# print(train_images.shape)
# print(type(train_labels))
# print(train_labels)

# Convert in grayscale np array images. From height*width*3 to height*width vector
test_images = np.asarray([rgb2gray(pi) for pi in test_images])

def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array, true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% \n ({})".format(CLASS_NAMES[int(predicted_label)],
                                100*np.max(predictions_array),
                                CLASS_NAMES[int(true_label)]),
                                color=color)

def showLossAcc(model):
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('\nTest loss:', test_loss)
    print('\nTest accuracy:', test_acc)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array, true_label[i]
  plt.grid(False)
  plt.xticks(range(len(CLASS_NAMES)), CLASS_NAMES, rotation='vertical')
  plt.yticks([])
  thisplot = plt.bar(range(len(CLASS_NAMES)), predictions_array, color="gray")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[int(true_label)].set_color('blue')

def loadModelSeq(modelName, weightName):
    json_file_name =modelName+'.json'
    print('Loading model from file: ' + json_file_name)
    json_file = open(join(models_dir, json_file_name), 'r')
    model_json = json_file.read()
    json_file.close()
    mymodel = model_from_json(model_json)
    mymodel.load_weights(join(models_dir, weightName+".h5"))
    return mymodel

def compileModel(model):
    model.compile(optimizer='adam', 
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
                  metrics=['accuracy'])
    return model

try:
    model
except NameError:
    # Type here the prefix of the model you want to load
    print('Loading model from file.')
    # model = loadModelSeq('modelSeq20200317131123ForwNormB', 'weightsSeq20200317131123ForwNormB')
    # model = loadModelSeq('modelSeq20200324222341AllFilled', 'weightsSeq20200324222341AllFilled')
    model = loadModelSeq('model'+modelName, 'weights'+modelName)

compileModel(model)
probability_model = keras.Sequential([model, keras.layers.Softmax()])
predictions = probability_model.predict(test_images)
print(predictions[0])
showLossAcc(model)

# Write here the index of the prediction you want to test
# i = 7
# print(predictions[i]) eg: array of pred [5.6500905e-03 9.8911971e-03 3.7678410e-10 9.8445868e-01]
# print(np.argmax(predictions[i])) eg: index label predicted 3
# plt.figure(figsize=(12,6))
# plt.subplot(1,2,1)
# plot_image(i, predictions[i], test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions[i],  test_labels)
# plt.show()
# Plot the first X test images, their predicted labels, and the true labels.
# Color correct predictions in blue and incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(10,10))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()