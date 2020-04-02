# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:05:39 2020

@author: e7470
"""
import matplotlib.pyplot as plt
from PIL import Image
import math

def cropImage(path, minX, maxX, minY, maxY, totalX, totalY):
  # print('Crop to: ' + str(minY) + " " + str(maxY) + " " + str(totalY))
  im = Image.open(path)
  widthOrig, heightOrig = im.size   # Get dimensions
  # print('Img size: ' + str(widthOrig) + "-" + str(heightOrig))

  X0 = -5 + widthOrig * minX / totalX
  Y0 = heightOrig - 5 - (heightOrig) * maxY / totalY
  X1 = widthOrig * (maxX + 2) / totalX
  Y1 = heightOrig + 5 - (heightOrig + 1) * minY / totalY

  # Crop the center of the image
  # (Xo, Y0, H, W)
  return im.crop((X0, Y0, X1, Y1))

def removePeaks(values, limitValue):
    values[0]=limitValue
    for i in range(len(values)-1):
        if (i > 0 and i < len(values) and (values[i] > limitValue or values[i] <= 0.0)):
            values[i] = values[i-1]

def plotLine(x_number_values, values, label):
    plt.plot(x_number_values, values, linewidth=1, label=label)
    plt.axis('equal')
    plt.legend()

def setupTitles(title, xlable, ylabel):
    plt.title(title, fontsize=19)
    plt.xlabel(xlable, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.tick_params(axis='both', labelsize=9)

def revertThePoints(points, maxValue):
    # Revert Right Points
    k = 0
    for i in points:
        points[k] = (points[k] * 100 - maxValue*100) * -1 / 100
        k += 1

# Remove all the possible extra space from the plot
def removeExtraSpaceInGraph():
  plt.gca().set_axis_off()
  plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
  plt.margins(0,0)
  plt.gca().xaxis.set_major_locator(plt.NullLocator())
  plt.gca().yaxis.set_major_locator(plt.NullLocator())
  
def getXaxesValues(y):
  x = []
  for i in range(len(y)):
    x.append(i)
  return x

def getFillAreaAndEdges(firstLine, secondLine):
     # Impossible to put the condition inside the fill_between function. It doesn't work
    fillArea = []
    firstX = 0
    lastX = 0
    
    for i in range(0, len(firstLine)):
      test = firstLine[i]<secondLine[i]
      if (test == True and firstX == 0): firstX = i
      if (test == True): lastX = i
      fillArea.append(test)
    return [fillArea, firstX, lastX]

def resize_canvas(old_image_path, new_image_path,
                  canvas_width, canvas_height):
    """
    Resize the canvas of old_image_path.
    https://stackoverflow.com/questions/1572691/in-python-python-image-library-1-1-6-how-can-i-expand-the-canvas-without-resiz/27784150#27784150
    Store the new image in new_image_path. Center the image on the new canvas.

    Parameters
    ----------
    old_image_path : str
    new_image_path : str
    canvas_width : int
    canvas_height : int
    """
    im = Image.open(old_image_path)
    old_width, old_height = im.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))
    newImage.save(new_image_path)