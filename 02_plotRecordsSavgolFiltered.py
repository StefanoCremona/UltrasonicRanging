#!/usr/bin/python
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import csv

limitValue = 89
maxValue = 89
delta=0
# Parse the string values from first file reading
def parseValues(x):
  return float(str.strip(x)) if len(x) > 0 else limitValue # Last value in line is usually empty

def removePeaks(values):
  for i in range(len(values)-1):
      if (i > 0 and i < len(values) and values[i] > (limitValue - delta)):
        values[i] = values[i-1]

def normaliseValues(values):
  for i in range(len(values)-1):
    if (i > 0 and i < len(values) and abs(values[i-1]-values[i+1]) < 10 and limitValue - values[i] < 10):
      values[i] = (values[i-1] + values[i+1]) / 2
    
# Plot a line based on the x and y axis value list.
def draw_line():

    f = open("Left.txt", "r")
    f1 = f.read()
    points = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()
    removePeaks(points[0])
    # normaliseValues(points[0])

    f = open("Right.txt", "r")
    f1 = f.read()
    pointsRight = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()
    removePeaks(pointsRight[0])
    # normaliseValues(pointsRight[0])

    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()

    # Create the X axes points and normalise them
    x_number_values = []
    k = 0
    for i in points[0]:
        x_number_values.append(k)
        # if (k > 0 and (i > 200 or i <= 5)):
        #    points[0][k] = points[0][k-1]
        k += 1

    # normaliseValues(points[0])
    # Normalise the Right points
    # k = 0
    # for i in pointsRight[0]:
    #     if (k > 0 and (i > 200 or i <= 5)): 
    #         pointsRight[0][k] = pointsRight[0][k-1]
    #     k += 1

    # Revert the right points
    k = 0
    for i in pointsRight[0]:
        pointsRight[0][k] = (pointsRight[0][k] * 100 - (maxValue+delta)*100) * -1 / 100
        k += 1

    #for y_number_values in points: 
    firstLine = savgol_filter(points[0], 3, 1)
    plt.plot(x_number_values, firstLine, linewidth=1, label="Left")
    plt.legend()


    # for y_number_values in pointsRight:
    secondLine = savgol_filter(pointsRight[0], 3, 1)
    plt.plot(x_number_values, secondLine, linewidth=1, label="Right")
    plt.legend()


    plt.fill_between(x_number_values, firstLine, secondLine, where=secondLine >= firstLine )
    #for x in f1:
    #    print map(str.strip, x.split(','))
    #print [map(str.strip, s_inner.split(',')) for s_inner in f1.splitlines()]
    #f.close()
    # List to hold x values.

    # List to hold y values.
    #y_number_values = [5.22,5.18,5.19,5.22,5.24,5.17,5.25]

    # Plot the number in the list and set the line thickness.
    #plt.plot(x_number_values, y_number_values, linewidth=1)

    # List to hold y values.
    #y_number_values2 = [5.18,5.24,5.23,5.22,5.22,5.17,5.19]

    # Plot the number in the list and set the line thickness.
    #plt.plot(x_number_values, y_number_values2, linewidth=1)

    # Set the line chart title and the text font size.
    plt.title("Ultrasonic records with filters", fontsize=19)

    # Set x axes label.
    plt.xlabel("Time (ms)", fontsize=10)

    # Set y axes label.
    plt.ylabel("Distance (cm)", fontsize=10)

    # Set the x, y axis tick marks text size.
    plt.tick_params(axis='both', labelsize=9)

    # Display the plot in the matplotlib's viewer.
    plt.show()

if __name__ == '__main__':
    draw_line()
