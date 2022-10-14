#!/usr/bin/python3

import csv


num=60
abs_value=-162000
outputlines = f'1file_output_lines'
file = f'out_data{num}'
i=0


with open(outputlines,'w') as wr:
    with open(file,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=" ")
        conv_abs_value1=abs_value/1000000
        conv_abs_value=float(conv_abs_value1)
        for row in csvreader:
            i+=1
            data_point=float(row[1])
            conv_i=str(i)
            if data_point >= conv_abs_value:
                wr.write(f'NR=={conv_i} || ')
            else:
                pass



