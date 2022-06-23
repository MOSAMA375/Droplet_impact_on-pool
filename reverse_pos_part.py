#!/usr/bin/python3

import os
import csv
import time

# csv file name
istep = '{istep = 1}'
filename = "input.csv"
# collect names
num = 380
end = 100
dt = 0.001

test = f'test'
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
            with open(f'test/t{f_num}/temp_out{i}', 'r') as f:
                output.write(f.readlines()[1])


check_folder(test)


# reading csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=" ")

    converted_num = str(num)
    out_data = f'test/out_data{converted_num}' 
    out_counter = 1
    out_folder = f'test/t{num}'
    check_folder(out_folder)

    for row in csvreader:
        gerris_2D(out_folder, out_counter, f'{row[0]} {row[1]} {row[2]}', num)
        out_counter = out_counter + 1

    # collect temp otput in a single file
    collect_output(out_data, out_counter, num)
        
for file_num in range(num, end, -1):
    read_data = f'test/out_data{file_num}'
    converted_num = str(file_num)

    with open(read_data, 'r') as csv_out:
        out_counter = 1
        out_folder = f'test/t{file_num - 1}'
        check_folder(out_folder)

        next_out_data = f'test/out_data{file_num - 1}'

        out_reader = csv.reader(csv_out, delimiter=" ")

        for r in out_reader:
            x = float(r[1]) - float(r[8]) * dt
            y = float(r[2]) - float(r[9]) * dt
            gerris_2D(out_folder, out_counter, f'{x} {y} 0', file_num - 1)
            out_counter = out_counter + 1

        collect_output(next_out_data, out_counter, file_num - 1)
    time.sleep(2)    #### Time delaying to avoid crash

file = 'output'
if(os.path.exists(file)):
    os.remove(file)

for n in range(num, end - 1, -1):
    with open(file, 'a') as output:
        with open(f'test/out_data{n}', 'r') as read:
            for line in read:
                output.write(line)

for n in range(num, end - 1, -1):
    os.system( f'rm -r test/t{n}')
