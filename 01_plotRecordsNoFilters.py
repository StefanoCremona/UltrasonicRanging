#!/usr/bin/python
import matplotlib.pyplot as plt
import csv

#x_number_values = [1, 2, 3, 4, 5, 6, 7]
maxDistance = 89 # 4 for Unity simulator, 22 real case

# Parse the string values from first file reading
def parseValues(x):
  return float(str.strip(x)) if len(x) > 0 else maxDistance # Last value in line is usually empty


# Plot a line based on the x and y axis value list.
def draw_line():

    f = open("Left.txt", "r")
    f1 = f.read()
    points = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    f = open("Right.txt", "r")
    f1 = f.read()
    pointsRight = [map(parseValues, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()

    # Create the X axes points and normalise them
    x_number_values = []
    k = 0
    for i in points[0]:
        x_number_values.append(k)
        # if (k > 0 and (i > maxDistance or i <= 5)):
        #     points[0][k] = points[0][k-1]
        k += 1

    # Normalise the Right points
#    k = 0
#    for i in pointsRight[0]:
#        if (k > 0 and (i > maxDistance or i <= 5)): 
#            pointsRight[0][k] = pointsRight[0][k-1]
#        k += 1

    # Revert the right points
#    k = 0
#    for i in pointsRight[0]:
#        pointsRight[0][k] = (pointsRight[0][k] * 100 -maxDistance*100) * -1 / 100
#        k += 1

    # print(points[0])
    # print(pointsRight[0])

    for y_number_values in points: 
        plt.plot(x_number_values, y_number_values, linewidth=1, label="Left")
        plt.legend()

    for y_number_values in pointsRight:
        plt.plot(x_number_values, y_number_values, linewidth=1, label="Right")
        plt.legend()

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
    plt.title("Ultrasonic records without filters", fontsize=19)

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
