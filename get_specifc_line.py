#!/usr/bin/python3

import linecache

num = 0
end = 1
file = 'output'

for file_num in range(num, end, 1):
    with open(file, 'a') as output:
        read_data = f'out_data{file_num}'
        with open(read_data, 'r') as input:
            particular_line = input.readlines()[4276]
            print(particular_line)
            output.write(particular_line)
