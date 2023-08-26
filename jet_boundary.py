#!/usr/bin/python3
import os
import subprocess
import tempfile
import shutil

tmp = tempfile.mkdtemp()

open("curvature.dat", "w").close()

# Create a file to write the output
output_file = open("output.txt", "w")

for i in range(10):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                t = f"{i}.{j}{k}{l}"
                file_name = f"i-{i}.{j}{k}{l}.gnu"
                
                if os.path.isfile(file_name):
                    subprocess.run(['awk', '$1 >= -0.43 && $2 >= -0.44 {print $1, $2}', file_name],
                                   stdout=open(f"{tmp}/out", "w"))
                    
                    with open(f"{tmp}/out", "r") as out_file:
                        X_max = max([float(line.split()[0]) for line in out_file])
                    
                    subprocess.run(['awk', f'$1 == {X_max} {{print $2}}', f"{tmp}/out"],
                                   stdout=open(f"{tmp}/out2", "w"))
                    
                    with open(f"{tmp}/out2", "r") as out2_file:
                        Y_req = next(out2_file).strip()
                    
                    with open(file_name, "r") as original_file:
                        lines = original_file.readlines()
                        line_num = next((index for index, line in enumerate(lines) if line.startswith(f"{X_max} ")), None)
                        num_lines = len(lines)
                    
                    if line_num is not None and line_num < len(lines):
                        lines = lines[line_num:]
                        lines = [line for line in lines if len(line.split()) >= 2 and float(line.split()[0]) > -0.43]
                        if lines:
                            Y_min = min([float(line.split()[1]) for line in lines])
                            with open(f"{tmp}/out3", "w") as out3_file:
                                out3_file.writelines(lines)
                            subprocess.run(['awk', f'$2 == {Y_min} {{print $1}}', f"{tmp}/out3"],
                                           stdout=open(f"{tmp}/out4", "w"))
                            with open(f"{tmp}/out4", "r") as out4_file:
                                X_req = next(out4_file).strip()

                            # Write the calculated values to the output file
                            output_file.write(f"{t} {X_max} {Y_req} {X_req} {Y_min}\n")

# Close the output file
output_file.close()

# Remove the temporary directory and its contents
shutil.rmtree(tmp)
