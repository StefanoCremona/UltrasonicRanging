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

# Plot a line based on the x and y axis value list.
def draw_line(path, timeRecording, laserHeight):

    f = open(path+timeRecording+"Left"+laserHeight+".txt", "r")
    f1 = f.read()
    points = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    f = open(path+timeRecording+"Right"+laserHeight+".txt", "r")
    f1 = f.read()
    pointsRight = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()
    
    filteredPoints = trimValues(points[0], pointsRight[0])

    firstLine = filteredPoints[0]  # use points[0] for row data or filteredPoints[0]
    secondLine = filteredPoints[1] # use rightPoints[0] for row data or filteredPoints[1]

    # Create the X axes points and normalise them
    x_number_values = []
    k = 0
    for i in firstLine:
        x_number_values.append(k)
        k += 1

    # Revert the right points
    k = 0
    for i in secondLine:
        secondLine[k] = (secondLine[k] * 100 - maxValue*100) * -1 / 100
        k += 1

    imgName = timeRecording if timeRecording else "foo"
    
    # Draw the lines with the default colors: 
    plt.plot(x_number_values, firstLine, linewidth=1)
    plt.plot(x_number_values, secondLine, linewidth=1)
    plt.savefig(path+imgName+laserHeight+'row.png', bbox_inches='tight', pad_inches=0)
    plt.clf() # Clear the cache
    
    # for y_number_values in points: 
    plt.plot(x_number_values, firstLine, linewidth=2, color=leftColor)

    # for y_number_values in pointsRight:
    plt.plot(x_number_values, secondLine, linewidth=2, color=rightColor)

    # Get the area to fill
    # Impossible to put the condition inside the fill_between function. It doesn't work
    fillArea = []

    for i in range(0, len(x_number_values)):
      test = firstLine[i]<secondLine[i]
      fillArea.append(test)

    plt.fill_between(x_number_values, firstLine, secondLine, where=fillArea, color=fillColor)

    # Remove all the possible extra space from the plot
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    plt.savefig(path+imgName+laserHeight+'filled.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    # Save the image in a squared form
    imgSize = getSize()
    maxSize = int(imgSize[0] if (imgSize[0] > imgSize[1]) else imgSize[1]) + 1
    resize_canvas(path+imgName+laserHeight+'filled.png', path+imgName+laserHeight+'squared.png', maxSize, maxSize)

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
