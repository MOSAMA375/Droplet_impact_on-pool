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
base=float(-0.499990)
zero=float(0)
h=float(1)

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

datapoints=f'test_{s}/datapoints{s}'

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=" ")
    with open(datapoints, 'a') as datainput: 
        for row in csvreader:
            x=row[0]
            y=row[1]
            datainput.write(f'{x} {y} {0} \n')

for file_num in range(num, num-1, -1):
    out_data=f'test_{s}/out_data{file_num}'
    datapoint=f'test_{s}/datapoints{file_num}'
    converted_num=str(file_num)
    os.system(f"gerris2D -e 'GfsOutputLocation {istep} {out_data} {datapoint}' snapshot-0.{converted_num.zfill(3)}.gfs >/dev/null")
    with open(out_data, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(out_data, 'w') as fout:
        fout.writelines(data[1:])
    

for file_num in range(num, num-2, -1):
    read_data = f'test_{s}/out_data{file_num}'
    converted_num = str(file_num-1)
    fnew_datapoint=f'test_{s}/datapoints{file_num-1}'
    next_out_data = f'test_{s}/out_data{file_num - 1}'

    with open(fnew_datapoint, 'a') as fdatainputs:
        with open(read_data, 'r') as csv_out:
            out_reader = csv.reader(csv_out, delimiter=" ")
            for r in out_reader:
                fl=float(r[13])
                if fl>zero:
                    x = float(r[1]) - float(r[8]) * dt
                    y = float(r[2]) - float(r[9]) * dt
                    fdatainputs.write(f'{x} {y} {0} \n')
                else:          
                    fdatainputs.write(f'{0} {0} {0} \n')
    os.system(f"gerris2D -e 'GfsOutputLocation {istep} {next_out_data} {fnew_datapoint}' snapshot-0.{converted_num.zfill(3)}.gfs >/dev/null")
    with open(next_out_data, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(next_out_data, 'w') as fout:
        fout.writelines(data[1:])


for file_num in range(num1, end, -1):
    read_data = f'test_{s}/out_data{file_num}'
    read_data1 = f'test_{s}/out_data{file_num-1}'
    read_data2 = f'test_{s}/out_data{file_num-2}'
    
    new_datapoint = f'test_{s}/datapoints{file_num-3}'
    next_out_data = f'test_{s}/out_data{file_num - 3}'
    converted_num = str(file_num-3)

    with open(new_datapoint, 'a') as datainputs:
        with open(read_data, 'r') as csv_out: 
            out_reader = csv.reader(csv_out, delimiter=" ")
            with open(read_data1, 'r') as csv_out1:  
                out_reader1 = csv.reader(csv_out1, delimiter=" ")
                with open(read_data2, 'r') as csv_out2:
                    out_reader2 = csv.reader(csv_out2, delimiter=" ")
                    for r in out_reader:
                        sec = next(out_reader1)
                        third = next(out_reader2)
                        f = float(third[13])
                        if f > zero:
                            ux1 = r[8]
                            uy1 = r[9]
                            ux2 = sec[8]
                            uy2 = sec[9]
                            ux3 = third[8]
                            uy3 = third[9]
                            x0 = third[1]
                            y0 = third[2]
                            x = float(x0) - h*(1.9166667*float(ux3)*dt-1.333333*float(ux2)*dt+0.4166667*float(ux1)*dt)
                            y = float(y0) - h*(1.1666667*float(uy3)*dt-1.333333*float(uy2)*dt+0.4166667*float(uy1)*dt)
                            if y <= base:
                                datainputs.write(f'{x} {-0.5} {0} \n')
                            else:
                                datainputs.write(f'{x} {y} {0} \n')
                        else:
                            datainputs.write(f'{0} {0} {0} \n')
    os.system(f"gerris2D -e 'GfsOutputLocation {istep} {next_out_data} {new_datapoint}' snapshot-0.{converted_num.zfill(3)}.gfs >/dev/null")
    with open(next_out_data, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(next_out_data, 'w') as fout:
        fout.writelines(data[1:])




