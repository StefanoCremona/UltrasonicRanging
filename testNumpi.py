import matplotlib.pyplot as plt
import csv

#x_number_values = [1, 2, 3, 4, 5, 6, 7]

# Plot a line based on the x and y axis value list.
def draw_line():

    f = open("walkingStef.txt", "r")
    f1 = f.read()
    points = [map(str.strip, s_inner.split(',')) for s_inner in f1.splitlines()]
    f.close()
    if (len(points) == 0):
        print("File empty. Ending program.")
        sys.exit()
    x_number_values = []
    k = 0
    for i in points[0]:
        x_number_values.append(k)
        k += 1

    for y_number_values in points: 
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
