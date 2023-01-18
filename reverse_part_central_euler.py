#!/usr/bin/python3

import os
import csv

# csv file name
s=63
istep = '{istep = 1}'
filename = f'sample_data_{s}'
# collect names
num = 63
num1=num
end = 1
two= float(2)
dt = 0.001

Test = f'test_{s}'
# initialize rows

def check_folder(folder_name: str):
    if(os.path.exists(folder_name)):
        print(f'{folder_name} already exists')
    else:
        os.mkdir(folder_name)

def gerris_2D(f_out_folder: str, f_out_counter: int, data_points: str, f_num: int):
    # print(f'DEBUG: {f_num}')
    converted_num = str(f_num)
    temp_out = f'{f_out_folder}/temp_out{f_out_counter}'
    # print(row, "0." + converted_num.zfill(3))
    # SEND input to geris
    os.system(
        f"gerris2D -e 'OutputLocation {istep} {temp_out} {data_points} ' snapshot-0.{converted_num.zfill(3)}.gfs > /dev/null")

def collect_output(f_out_data: str, f_out_counter: int, f_num: int):
    if(os.path.exists(f_out_data)):
        os.remove(f_out_data)

    with open(f_out_data, 'a') as output:
        for i in range(1, f_out_counter):
            with open(f'test_{s}/t{f_num}/temp_out{i}', 'r') as f:
                output.write(f.readlines()[1])


check_folder(Test)


# reading csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=" ")

    converted_num = str(num)
    out_data = f'test_{s}/out_data{converted_num}' 
    out_counter = 1
    out_folder = f'test_{s}/t{num}'
    check_folder(out_folder)

    for row in csvreader:
        gerris_2D(out_folder, out_counter, f'{row[0]} {row[1]} {row[2]}', num)
        out_counter = out_counter + 1

    # collect temp otput in a single file
    collect_output(out_data, out_counter, num)
        
for file_num in range(num, num-1, -1):
    read_data = f'test_{s}/out_data{file_num}'
    converted_num = str(file_num)

    with open(read_data, 'r') as csv_out:
        out_counter = 1
        out_folder = f'test_{s}/t{file_num - 1}'
        check_folder(out_folder)

        next_out_data = f'test_{s}/out_data{file_num - 1}'

        out_reader = csv.reader(csv_out, delimiter=" ")

        for r in out_reader:
            x = float(r[1]) - float(r[8]) * dt
            y = float(r[2]) - float(r[9]) * dt
            gerris_2D(out_folder, out_counter, f'{x} {y} 0', file_num - 1)
            out_counter = out_counter + 1

        collect_output(next_out_data, out_counter, file_num - 1)

for file_num in range(num1, end, -1):
    read_data = f'test_{s}/out_data{file_num}'
    read_data1= f'test_{s}/out_data{file_num-1}'
    converted_num = str(file_num)

    with open(read_data, 'r') as csv_out:
        out_counter = 1
        out_folder = f'test_{s}/t{file_num - 2}'
        check_folder(out_folder)
        next_out_data = f'test_{s}/out_data{file_num - 2}'
        out_reader = csv.reader(csv_out, delimiter=" ")
        with open(read_data1, 'r') as csv_out1:  
            out_reader1 = csv.reader(csv_out1, delimiter=" ")
            for r in out_reader:
                l=next(out_reader1)
                x0=r[1]
                y0=r[2]
                ux=l[8]
                uy=l[9]
                x = float(x0) - float(ux)*two*dt
                y = float(y0) - float(uy)*two*dt
                print(f'{x} {y}') 
                gerris_2D(out_folder, out_counter, f'{x} {y} 0', file_num - 2)
                out_counter = out_counter + 1
            collect_output(next_out_data, out_counter, file_num - 2)

file = 'output'
if(os.path.exists(file)):
    os.remove(file)

for n in range(num, end - 1, -1):
    with open(file, 'a') as output:
        with open(f'test_{s}/out_data{n}', 'r') as read:
            for line in read:
                output.write(line)

for n in range(num, end - 1, -1):
    os.system( f'rm -r test_{s}/t{n}')
