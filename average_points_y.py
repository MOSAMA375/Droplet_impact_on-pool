#!/usr/bin/python3

import os
import csv
import math
from math import *

num = 10
end = 32
gap=1
filename=f'out_data0'
output1=f'averages'

for file_num in range(num, end, 2):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=" ")
        with open(output1, 'a') as output:
            i=0
            sum=0
            for r in csvreader:
                x1=float(r[1])
                y1=float(r[2])
                x= float((-57.3*atan((x1+0.5)/(y1+0.5-0.141))))
                y=float((0.1-(sqrt((x1+0.5)**2+(y1+0.5-0.141)**2))))
                xlim1=float(file_num+gap)
                xlim2=float(file_num-gap)
                if x<xlim1 and x>xlim2 and y>0:
                    sum+=y
                    i+=1
            output.write(f' {file_num} {sum} {i} \n')
            
