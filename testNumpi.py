import matplotlib.pyplot as plt
import csv

#x_number_values = [1, 2, 3, 4, 5, 6, 7]

# Plot a line based on the x and y axis value list.
def draw_line():

    f = open("walkingStef.txt", "r")
    f1 = f.read()
    points = [map(lambda x: float(str.strip(x)), s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    f = open("walkingStefRight.txt", "r")
    f1 = f.read()
    pointsRight = [map(lambda x: float(str.strip(x)), s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()

    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()

    # Create the X axes points and normalise them
    x_number_values = []
    k = 0
    for i in points[0]:
        x_number_values.append(k)
        if (k > 0 and (i > 200 or i <= 5)):
            points[0][k] = points[0][k-1]
        k += 1

    # Normalise the Right points
    k = 0
    for i in pointsRight[0]:
        if (k > 0 and (i > 200 or i <= 5)): 
            pointsRight[0][k] = pointsRight[0][k-1]
        k += 1

    # Revert the right points
    k = 0
    for i in pointsRight[0]:
        pointsRight[0][k] = (pointsRight[0][k] * 100 -19500) * -1 / 100
        k += 1

    print(points[0])
    print(pointsRight[0])

    for y_number_values in points: 
        plt.plot(x_number_values, y_number_values, linewidth=1)

    for y_number_values in pointsRight:
        plt.plot(x_number_values, y_number_values, linewidth=1)

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
    plt.title("Square Numbers", fontsize=19)

    # Set x axes label.
    plt.xlabel("Number Value", fontsize=10)

    # Set y axes label.
    plt.ylabel("Sonic Pings", fontsize=10)

    # Set the x, y axis tick marks text size.
    plt.tick_params(axis='both', labelsize=9)

    # Display the plot in the matplotlib's viewer.
    plt.show()

if __name__ == '__main__':
    draw_line()
