#!/usr/bin/python3

from shapely.geometry import Point, Polygon
import warnings

# Read in interface data
with open('interface_data.txt', 'r') as f:
    interface_coords = []
    for line in f:
        # Split the line into fields and convert each field to a float
        fields = line.split()
        x, y = map(float, fields)
        # Append the x and y coordinates to the interface_coords list
        interface_coords.append((x, y))

# Create a Shapely polygon from the interface coordinates
interface_poly = Polygon(interface_coords)
if not interface_poly.is_valid:
    interface_poly = interface_poly.buffer(0)

# Read in particle coordinates data
with open('particle_coordinates.txt', 'r') as f:
    particles = []
    for line in f:
        # Ignore empty lines
        if line.strip():
            # Split the line into fields and convert the first two fields to floats
            fields = line.split()
            x, y = map(float, fields)
            # Append the x and y coordinates to the particles list as a Shapely Point object
            particles.append(Point(x, y))

# Check each particle's position relative to the interface polygon
shared_particles = []
for particle in particles:
    # Create a small circle centered on the particle using the Shapely buffer() method
    particle_circle = particle.buffer(0.001)
    # Suppress the runtime warning for invalid intersections
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Find the intersection between the particle circle and the interface polygon using the Shapely intersection() method
        intersection = particle_circle.intersection(interface_poly)
    # If the intersection is not empty, the particle is within the interface region
    if not intersection.is_empty:
        shared_particles.append(particle)

# Write out the shared particle coordinates
with open('shared_particles.txt', 'w') as f:
    for particle in shared_particles:
        # Write out only the x and y coordinates
        f.write('{} {}\n'.format(particle.x, particle.y))
