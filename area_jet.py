#!/usr/bin/python3
import os
import numpy as np
from shapely.geometry import Point, Polygon
import warnings

os.system('mkdir COMPOSITIONS')
def area(coordinates):

    n = len(coordinates)
    area = 0.0
    j = n - 1

    for i in range(n):
        area += (coordinates[j][0] + coordinates[i][0]) * (coordinates[j][1] - coordinates[i][1])
        j = i
    return abs(area/2.0)

for i in range(1):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                t = f"{i}.{j}{k}{l}"
                FILE = f"Jet{t}/nj-{t}.gnu"
                FILE1= f"Drop/i-{t}.gnu"
                data_f=f"COMPOSITIONS/drop_composition"
                if os.path.isfile(FILE):
                    with open(FILE1, "r") as infile, open(f"Drop/d-{t}.gnu", "w") as outfile:
                        for line in infile:
                            columns = line.split()
                            if len(columns) >= 2:
                                outfile.write(f"{columns[0]} {columns[1]}\n")
                    with open(FILE, 'r') as f:
                        interface_coords = []
                        for line in f:
                            fields = line.split()
                            x, y = map(float, fields)
                            interface_coords.append((x, y))
                    interface_poly = Polygon(interface_coords)
                    if not interface_poly.is_valid:
                        interface_poly = interface_poly.buffer(0)
                    with open(f"Drop/d-{t}.gnu", 'r') as f:
                        particles = []
                        for line in f:
                            if line.strip():
                                fields = line.split()
                                x, y = map(float, fields)
                                particles.append(Point(x, y))
                    shared_particles = []
                    for particle in particles:
                        particle_circle = particle.buffer(0.001)
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            intersection = particle_circle.intersection(interface_poly)
                        if not intersection.is_empty:
                            shared_particles.append(particle)
                    with open(f'Jet{t}/shared_part{t}', 'w') as f:
                        for particle in shared_particles:
                            f.write('{} {}\n'.format(particle.x, particle.y))
                    with open(f'Jet{t}/shared_part{t}', "r") as file:
                        first_line = file.readline()
                    with open(f'Jet{t}/shared_part{t}', "a") as file:
                        file.write(first_line)
                    with open(f'Jet{t}/shared_part{t}', 'r') as file:
                        coordinates = [tuple(map(float, line.strip().split())) for line in file]
                    surface_area = area(coordinates)
                    with open(FILE, 'r') as file:
                        coordinatesjet = [tuple(map(float, line.strip().split())) for line in file]
                    surface_area1 = area(coordinatesjet)
                    ratio=((surface_area/surface_area1))
                    with open(data_f, "a") as final:
                        final.write(f"{t} {surface_area} {surface_area1} {ratio} \n")
