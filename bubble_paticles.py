#!/usr/bin/python3

import os
import csv
import math
from math import *
import numpy


filename=f'out_data0'
output1=f'input_data'
h=float(0.1031)

with open(output1, 'a') as output:
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=" ")
        for r in csvreader:
            x1=float(r[1])
            y1=float(r[2])
            y=float((0.1-(sqrt((x1+0.5)**2+(y1+0.5-h)**2))))
            if y>0:
                output.write(f' {x1} {y1} {0} \n')
