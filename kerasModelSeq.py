# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:33:12 2020

@author: e7470
"""
# train_images = train_images / 255.0
# test_images = test_images / 255.0
import keras
from keras.models import Sequential, model_from_json
from keras.layers import Conv2D, MaxPool2D, Dropout, Dense, Flatten, MaxPooling2D

print(train_images.shape)
print(train_labels.shape)

num_classes=len(CLASS_NAMES)
image_size = 784 # 28*28

def fitModel(model):
    model.fit(train_images, train_labels, epochs=100)
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('\nTest loss:', test_loss)
    print('\nTest accuracy:', test_acc)

def model1():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy'])
    return model

def getDataModel2(x_train, y_train, x_test, y_test):
  img_rows, img_cols = 28, 28

  #Preprocessin for model 2
  x2_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
  x2_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)

  x2_train = x2_train.astype('float32')
  x2_test = x2_test.astype('float32')
  x2_train /= 255
  x2_test /= 255
  print('x_train shape:', x2_train.shape)
  print(x2_train.shape[0], 'train samples')
  print(x2_test.shape[0], 'test samples')

  # convert class vectors to binary class matrices
  y2_train = keras.utils.to_categorical(y_train, num_classes)
  y2_test = keras.utils.to_categorical(y_test, num_classes)
  return x2_train, y2_train, x2_test, y2_test

def model2():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy']) #, 'mean_absolute_error', 'mean_squared_error'])
    return model

fitModel(model1())
#getDataModel2(train_images, train_labels, test_images, test_labels)