# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:43:54 2020

@author: e7470
"""
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

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array, true_label[i]
  plt.grid(False)
  plt.xticks(range(len(CLASS_NAMES)), rotation='vertical')
  plt.yticks([])
  thisplot = plt.bar(range(len(CLASS_NAMES)), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[int(true_label)].set_color('blue')

probability_model = keras.Sequential([model, keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

i = 15
print(predictions[i])
print(np.argmax(predictions[i]))

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()