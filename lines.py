#!/usr/bin/python3

import csv


num=200
abs_value=3
outputlines = f'file_output_lines'
file = f'outdata{num}'
i=0


with open(outputlines,'w') as wr:
    with open(file,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=" ")
        conv_abs_value=str(abs_value)
        for row in csvreader:
            i+=1
            data_point=row[1]
            conv_i=str(i)
            if data_point < conv_abs_value:
                wr.write(f'NR=={conv_i} || ')
            else:
                pass
            


