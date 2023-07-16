#!/usr/bin/python3


def area(coordinates):
    """
    This function calculates the area inside of an irregular surface using the Shoelace Formula.
    The input is a list of tuples, where each tuple contains the x and y coordinates of a point on the surface.
    """
    n = len(coordinates)
    area = 0.0
    j = n - 1

    for i in range(n):
        area += (coordinates[j][0] + coordinates[i][0]) * (coordinates[j][1] - coordinates[i][1])
        j = i

    return abs(area/2.0)


# Open the file containing the coordinates
with open('coordinates.txt', 'r') as file:
    # Extract the coordinates into a list of tuples
    coordinates = [tuple(map(float, line.strip().split())) for line in file]

# Call the area function with the coordinates list
surface_area = area(coordinates)

# Print the area of the irregular surface
print(f"The area of the irregular surface is: {surface_area}")
