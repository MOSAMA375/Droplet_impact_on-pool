#!/usr/bin/python3
import os
import numpy as np
from shapely.geometry import Point, Polygon
import warnings

for i in range(1):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                t = f"{i}.{j}{k}{l}"
                name = int(f"{j}{k}{l}")  # Convert to integer
                n1 = j
                n2 = k
                n3 = l
                FILE = f"nj-{t}.gnu"
                if os.path.isfile(FILE):
                    # Initialize variables for each new file
                    x_min = float('inf')
                    x_max = float('-inf')
                    y_min = float('inf')
                    y_max = float('-inf')
                    
                    with open(FILE, 'r') as file:
                        for line in file:
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                x_value, y_value = map(float, parts[:2])
                                if x_value < x_min:
                                    x_min = x_value
                                if x_value > x_max:
                                    x_max = x_value
                                if y_value < y_min:
                                    y_min = y_value
                                if y_value > y_max:
                                    y_max = y_value
                    start_x = x_min
                    stop_x = x_max + 0.000061
                    step_x = 0.000061

                    start_y = y_min
                    stop_y = y_max + 0.000061
                    step_y = 0.000061

                    output = f'particle_coordinates{i}{j}{k}{l}.txt'

                    with open(output, 'w') as f:
                        for i in np.arange(start_x, stop_x, step_x):
                            for j in np.arange(start_y, stop_y, step_y):
                                f.write(f'{i} {j}\n')
                    
                    with open(FILE, 'r') as f:
                        interface_coords = []
                        for line in f:
                            fields = line.split()
                            x, y = map(float, fields)
                            interface_coords.append((x, y))

                    interface_poly = Polygon(interface_coords)
                    if not interface_poly.is_valid:
                        interface_poly = interface_poly.buffer(0)

                    with open(output, 'r') as f:
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
                    if name < 100:
                        n = f"{n2}{n3}"
                    else:
                        n = f"{n1}{n2}{n3}"
                    with open(f'sample_data_{n}.txt', 'w') as f:
                        for particle in shared_particles:
                            f.write('{} {}\n'.format(particle.x, particle.y))
                    os.system(f'rm {output}')
                else:
                    pass
