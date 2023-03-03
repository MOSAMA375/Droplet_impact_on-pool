#!/usr/bin/python3

import csv
import os

os.system(f'mkdir Lines')

start=16
end = 15
i=0
newfile=f'minimumpoints'

with open(newfile,'r') as r:
    csvreader1 = csv.reader(r, delimiter=" ")
    for rows in csvreader1:
        limit_x=float(rows[0])
        limit_y=float(rows[1])
        for file_num in range(start, end, -1):
            outputlines = f'Lines/file_output_lines{file_num}'
            file = f'out_data{file_num}'
            with open(outputlines,'w') as wr:
                with open(file,'r') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=" ")
                    for row in csvreader:
                        i+=1
                        data_point_x=float(row[1])
                        data_point_y=float(row[2])
                        conv_i=str(i)
                        if data_point_x <= limit_x and data_point_y>= limit_y:
                            wr.write(f'NR=={conv_i} || ')
                        else:
                            pass
                    
