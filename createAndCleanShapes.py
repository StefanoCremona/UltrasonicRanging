#!/c/Python27/python.exe
import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image
import math
import PIL
import sys
from PIL import Image

#x_number_values = [1, 2, 3, 4, 5, 6, 7]
leftColor="white"
rightColor="white"
fillColor="black"
maxValue=4 # 4 for Unity simulator, 22 real case
deltaValue=0.3

# Parse the string values from first file reading
def parseValues(x):
  return float(str.strip(x)) if len(x) > 0 else maxValue # Last value in line is usually empty

def getSize():
  fig = plt.gcf()
  return fig.get_size_inches()*fig.dpi

def getXaxesValues(y):
  x = []
  for i in range(len(y)):
    x.append(i)
  return x

# Revert the point by maxvalue through the y axes
def revertPoints(myArray):
  retVal = []
  for i in range(len(myArray)):
    retVal.append((myArray[i] * 100 - maxValue*100) * -1 / 100)
  return retVal

# Draw the lines with the default colors: 
def drawChartAndSaveImg(line1, line2, imgNameAndPath):
    x = getXaxesValues(line1)
    plt.plot(x, line1, linewidth=1)
    plt.plot(x, line2, linewidth=1)

    # plt.show()
    plt.savefig(imgNameAndPath, bbox_inches='tight', pad_inches=0)
    plt.clf() # Clear the cache

def getInterceptions(line1, line2):
    line1A = np.array(line1)
    line2A = np.array(line2)

    return len(np.argwhere(np.diff(np.sign(line1A - line2A))).flatten())

def getPointsFromFile(path):
  f = open(path, "r")
  f1 = f.read()
  points = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
  f.close()
  return points

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

# Remove initial and ending useless values
def trimValues(points, pointsRight):
  maxLen=len(points)
  left = 0
  right=maxLen
  for i in range(maxLen):
    if (points[i] < (maxValue - deltaValue) or pointsRight[i] < (maxValue - deltaValue)):
      left=i
      break
  for i in range(maxLen):
    if (points[maxLen-i-1] < (maxValue - deltaValue) or pointsRight[maxLen-i-1] < (maxValue - deltaValue)):
      right=maxLen-i
      break
  
  return [points[left:right], pointsRight[left:right]]

# Remove all the possible extra space from the plot
def removeExtraSpaceInGraph():
  plt.gca().set_axis_off()
  plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
  plt.margins(0,0)
  plt.gca().xaxis.set_major_locator(plt.NullLocator())
  plt.gca().yaxis.set_major_locator(plt.NullLocator())

def cropImage(imgPrefix, imgSuffix, minX, maxX, minY, maxY, totalX, totalY):
  # print('Crop to: ' + str(minY) + " " + str(maxY) + " " + str(totalY))
  im = Image.open(imgPrefix + imgSuffix)
  widthOrig, heightOrig = im.size   # Get dimensions
  # print('Img size: ' + str(widthOrig) + "-" + str(heightOrig))

  X0 = -5 + widthOrig * minX / totalX
  Y0 = heightOrig - 5 - (heightOrig) * maxY / totalY
  X1 = widthOrig * (maxX + 2) / totalX
  Y1 = heightOrig + 5 - (heightOrig + 1) * minY / totalY

  # Crop the center of the image
  # (Xo, Y0, H, W)
  return im.crop((X0, Y0, X1, Y1))

# Plot a line based on the x and y axis value list.
def draw_line(path, timeRecording, laserHeight):

    points = getPointsFromFile(path+timeRecording+"Left"+laserHeight+".txt")
    pointsRight = getPointsFromFile(path+timeRecording+"Right"+laserHeight+".txt")

    if (len(points) == 0 or len(pointsRight) == 0):
        print("A File with "+timeRecording+" prefix is empty. Ending program.")
        sys.exit()
    
    imgName = timeRecording if timeRecording else "foo"

    # Draw the lines with the default colors:
    removeExtraSpaceInGraph()
    drawChartAndSaveImg(points[0], revertPoints(pointsRight[0]), path+imgName+laserHeight+'row.png')
    
    # Filtering stretch the image
    # filteredPoints = trimValues(points[0], pointsRight[0])

    firstLine = points[0]  # use points[0] for row data or filteredPoints[0]
    secondLine = pointsRight[0] # use rightPoints[0] for row data or filteredPoints[1]

    # Revert the right points
    secondLine = revertPoints(secondLine)

    minY = min(firstLine)
    maxY = max(secondLine)

    # Get the number of different shapes created by the interceptions of the 2 lines
    nShapes = getInterceptions(firstLine, secondLine) / 2

    # Get the area to fill
    # Impossible to put the condition inside the fill_between function. It doesn't work
    fillArea = []
    firstX = 0
    lastX = 0
    # Create the X axes points and normalise them
    x_number_values = getXaxesValues(firstLine)
    for i in range(0, len(x_number_values)):
      test = firstLine[i]<secondLine[i]
      if (test == True and firstX == 0): firstX = i
      if (test == True): lastX = i
      fillArea.append(test)

    crop = cropImage(path+imgName+laserHeight, 'row.png', firstX, lastX, minY, maxY, len(firstLine), max(firstLine))
    crop.save(path+imgName+laserHeight + "rowCrop.png")
    
    imgSize = crop.size
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(path+imgName+laserHeight+'rowCrop.png', path+imgName+laserHeight+'rowCropSquared'+str(nShapes)+'.png', maxSize, maxSize)

    # Draw the lines with the default colors:
    # drawChartAndSaveImg(firstLine, secondLine, path+imgName+laserHeight+'filtered.png')
    
    # Save the filled Images
    removeExtraSpaceInGraph()
    plt.plot(x_number_values, firstLine, linewidth=0, color=leftColor)
    plt.plot(x_number_values, secondLine, linewidth=0, color=rightColor)

    plt.fill_between(x_number_values, firstLine, secondLine, where=fillArea, color=fillColor)

    plt.savefig(path+imgName+laserHeight+'filled.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    crop = cropImage(path+imgName+laserHeight, 'filled.png', firstX, lastX, minY, maxY, len(firstLine), max(firstLine))
    crop.save(path+imgName+laserHeight + "crop.png")

    # Save the image in a squared form
    imgSize = crop.size
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(path+imgName+laserHeight+'crop.png', path+imgName+laserHeight+'squared'+str(nShapes)+'.png', maxSize, maxSize)

    # Resize it in a 28*28 for for the AI test
    # Not needed anymore because keras can do it
    """ img = Image.open(path+imgName+laserHeight+'squared.png')
    resized = img.resize((28, 28), PIL.Image.ANTIALIAS)
    resized.save(path+imgName+laserHeight+'resized28.png')

    # Resize it in a 56*56 for for the AI test
    # Not needed anymore because keras can do it
    resized = img.resize((56, 56), PIL.Image.ANTIALIAS)
    resized.save(path+imgName+laserHeight+'resized56.png') """

if __name__ == '__main__':
    draw_line("C:/Users/e7470/rowData/singleDouglasWalking" + "/", "202003101258314609", "M")
