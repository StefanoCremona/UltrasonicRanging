#!/usr/bin/python
import matplotlib.pyplot as plt
from plotRecordsUtils import removePeaks, plotLine, setupTitles, revertThePoints, removeExtraSpaceInGraph, getXaxesValues, getFillAreaAndEdges, cropImage, resize_canvas
from scipy.signal import savgol_filter
import sys
from os.path import join

#x_number_values = [1, 2, 3, 4, 5, 6, 7]
maxValue = 65 # 4 for Unity simulator

# Parse the string values from first file reading
def parseValues(x):
  return float(str.strip(x)) if len(x) > 0 else maxValue # Last value in line is usually empty

def readPoints(file):
    f = open(file, "r")
    f1 = f.read()[:-1] # I remove the last character that usually is a ','
    f.close()
    return [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]

def saveImageForModel(firstLine, secondLine, path, ratio):
    removeExtraSpaceInGraph()
    leftColor = rightColor = "white"
    fillColor = "black"
    minY = min(firstLine)
    maxY = max(secondLine)
    
    fillArea, firstX, lastX = getFillAreaAndEdges(firstLine, secondLine)
    
    x_values = getXaxesValues(firstLine)
    plt.plot(x_values, firstLine, linewidth=0, color=leftColor)
    plt.plot(x_values, secondLine, linewidth=0, color=rightColor)

    plt.fill_between(x_values, savgol_filter(firstLine, 3, 1), savgol_filter(secondLine, 3, 1), where=secondLine >= firstLine, color=fillColor)

    ax = plt.gca() #you first need to get the axis handle
    ax.set_aspect(ratio) #sets the height to width ratio to 1.5.

    plt.savefig(join(path, 'Filled.png'), bbox_inches='tight', pad_inches=0)
    plt.show()

    crop = cropImage(join(path, 'Filled.png'), firstX, lastX, minY, maxY, len(firstLine), max(firstLine))
    crop.save(join(path, "FilledCrop.png"))

    # Save the image in a squared form
    imgSize = crop.size
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(join(path, 'FilledCrop.png'), join(path, 'FilledCropSquared.png'), maxSize, maxSize)

# Plot a line based on the x and y axis value list.
def draw_line():

    points = readPoints("Left.txt")
    pointsRight = readPoints("Right.txt")

    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()

    # Create the X axes points and normalise them
    x_number_values = []
    k = 0
    for i in points[0]:
        x_number_values.append(k)
        k += 1

    plotLine(x_number_values, points[0], "Left")
    plotLine(x_number_values, pointsRight[0], "Right")

    setupTitles("Ultrasonic records without filters", "Time (ms)", "Distance (cm)")
    plt.show()

    plt.clf() # Clear the cache

    #Plot lines with savgol filter
    removePeaks(points[0], maxValue)
    removePeaks(pointsRight[0], maxValue)
    
    # Revert Right Points
    revertThePoints(pointsRight[0], maxValue)
    
    # Apply a transformation to have the curve smoother
    firstLine = savgol_filter(points[0], 3, 1)
    secondLine = savgol_filter(pointsRight[0], 3, 1)

    plotLine(x_number_values, firstLine, "Left")
    plotLine(x_number_values, secondLine, "Right")
    plt.fill_between(x_number_values, firstLine, secondLine, where=secondLine >= firstLine )
    
    aspectRatio = 0.5
    ax = plt.gca() #you first need to get the axis handle
    ax.set_aspect(aspectRatio) #sets the height to width ratio to 1.5.

    setupTitles("Ultrasonic records with filters", "Time (ms)", "Distance (cm)")
    
    plt.show()
    
    saveImageForModel(firstLine, secondLine, "./", aspectRatio)

if __name__ == '__main__':
    draw_line()
