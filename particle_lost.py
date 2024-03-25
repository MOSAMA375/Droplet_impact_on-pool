#!/usr/bin/python3

def calculate_percentage(filename):
    total_lines = 0
    count_zeros = 0

    with open(filename, 'r') as file:
        for line in file:
            total_lines += 1
            columns = line.strip().split()
            if len(columns) >= 3 and float(columns[1]) == 0 and float(columns[2]) == 0:
                count_zeros += 1
    
    percentage = (count_zeros / total_lines) * 100 if total_lines > 0 else 0

    return percentage

filename = "out_data0"
percentage = calculate_percentage(filename)
print(f"Percentage of rows where both column 2 and column 3 are zero: {percentage:.2f}%")




