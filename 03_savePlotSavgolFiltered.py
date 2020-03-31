#!/c/Python27/python.exe
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.signal import savgol_filter
from plotRecordsUtils import removePeaks, removeExtraSpaceInGraph, getXaxesValues, getFillAreaAndEdges, cropImage, resize_canvas
from os.path import join

#x_number_values = [1, 2, 3, 4, 5, 6, 7]
leftColor="white"
rightColor="white"
fillColor="black"
maxValue=89 # 4 for Unity simulator, 22 real case
deltaValue=0.3
delta = 0

# Parse the string values from first file reading
def parseValues(x):
  return float(str.strip(x)) if len(x) > 0 else maxValue # Last value in line is usually empty

def getSize():
  fig = plt.gcf()
  return fig.get_size_inches()*fig.dpi

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

def drawSavgolChartAndSaveImg(line1, line2, imgNameAndPath):
    x = getXaxesValues(line1)
    
    line1 = savgol_filter(line1, 3, 1)
    line2 = savgol_filter(line2, 3, 1)

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

# Plot a line based on the x and y axis value list.
def draw_line(path, timeRecording, laserHeight):

    points = getPointsFromFile(path+timeRecording+"Left"+laserHeight+".txt")
    pointsRight = getPointsFromFile(path+timeRecording+"Right"+laserHeight+".txt")

    removePeaks(points[0], maxValue)
    removePeaks(pointsRight[0], maxValue)

    if (len(points) == 0 or len(pointsRight) == 0):
        print("A File with "+timeRecording+" prefix is empty. Ending program.")
        sys.exit()
    
    imgName = timeRecording if timeRecording else "foo"

    # Draw the lines with the default colors:
    removeExtraSpaceInGraph()
    drawSavgolChartAndSaveImg(points[0], revertPoints(pointsRight[0]), path+imgName+laserHeight+'row.png')
    
    # Filtering stretch the image
    # filteredPoints = trimValues(points[0], pointsRight[0])

    firstLine = points[0]  # use points[0] for row data or filteredPoints[0]
    secondLine = pointsRight[0] # use rightPoints[0] for row data or filteredPoints[1]

    # Revert the right points
    secondLine = revertPoints(secondLine)

    minY = min(firstLine)
    maxY = max(secondLine)

    # Get the number of different shapes created by the interceptions of the 2 lines
    # nShapes = getInterceptions(firstLine, secondLine) / 2

    # Get the area to fill
    # Impossible to put the condition inside the fill_between function. It doesn't work    
    fillArea, firstX, lastX = getFillAreaAndEdges(firstLine, secondLine)

    crop = cropImage(join(path, imgName+laserHeight +'row.png'), firstX, lastX, minY, maxY, len(firstLine), max(firstLine))
    crop.save(path+imgName+laserHeight + "rowCrop.png")
    
    imgSize = crop.size
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(path+imgName+laserHeight+'rowCrop.png', path+imgName+laserHeight+'rowCropSquared.png', maxSize, maxSize)
    
    # Save the filled Images
    removeExtraSpaceInGraph()
    # Create the X axes points and normalise them
    x_number_values = getXaxesValues(firstLine)
    
    plt.plot(x_number_values, firstLine, linewidth=0, color=leftColor)
    plt.plot(x_number_values, secondLine, linewidth=0, color=rightColor)

    plt.fill_between(x_number_values, savgol_filter(firstLine, 3, 1), savgol_filter(secondLine, 3, 1), where=fillArea, color=fillColor)

    plt.savefig(path+imgName+laserHeight+'Filled.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    crop = cropImage(join(path, imgName+laserHeight+'Filled.png'), firstX, lastX, minY, maxY, len(firstLine), max(firstLine))
    crop.save(path+imgName+laserHeight + "FilledCrop.png")

    # Save the image in a squared form
    imgSize = crop.size
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(path+imgName+laserHeight+'FilledCrop.png', path+imgName+laserHeight+'FilledCropSquared.png', maxSize, maxSize)

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
    draw_line("C:/Users/e7470/Scripts" + "/", "", "")
