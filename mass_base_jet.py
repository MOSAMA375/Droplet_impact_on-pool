#!/usr/bin/python3

import os
import csv
import math 

ten=float(10)
eleven=float(11)
istep = '{istep = 1}'

os.mkdir("Mass")

for i in range(10):
    for j in range(10):
        for k in range(0, 10, 2):
            for l in range(10):
                for m in range(10):
                    t = f"{i}.{j}{k}{l}{m}"
                    t2=t
                    if t == "0.0000":
                        continue
                    FILE = f"Interface/Jet{t}/nj-{t}.gnu"
                    first_file=f"Mass/points-{t}"
                    out_data=f"Mass/out_data_{t}"
                    sum=0
                    final=f"Mass/mass_all"
                    if os.path.isfile(FILE):
                        if float(t) < 0.1000:
                            file_num = f"{k}{l}{m}"
                        else:
                            file_num = f"{j}{k}{l}{m}"
                        with open(FILE, "r") as file:
                            lines = file.readlines()
                        if len(lines) >= 2:
                            first_line = lines[0].strip().split()  
                            second_last_line = lines[-2].strip().split() 

                            x_first = float(first_line[0])  
                            y_first = float(first_line[1])  
                            x_second_last = float(second_last_line[0])  
                            y_second_last = float(second_last_line[1])

                            with open(first_file, "a") as w:
                                l=1
                                w.write(f"{x_first} {y_first} {0}\n")
                                for new in range(9):
                                    diff_x=abs(x_second_last-x_first)/ten
                                    diff_y=abs(y_second_last-y_first)/ten
                                    x_new=x_second_last+(diff_x*l)
                                    y_new=y_second_last-(diff_y*l)
                                    l+=1
                                    w.write(f"{x_new} {y_new} {0}\n")
                                w.write(f"{x_second_last} {y_second_last} {0}\n")

                            converted_num=str(file_num)
                            os.system(f"gerris2D -e 'GfsOutputLocation {istep} {out_data} {first_file}' snapshot-0.{converted_num.zfill(4)}.gfs >/dev/null")
                            with open(out_data, 'r') as fin:
                                data = fin.read().splitlines(True)
                            with open(out_data, 'w') as fout:
                                fout.writelines(data[1:])

                            with open(out_data, 'r') as csv_out: 
                                out_reader = csv.reader(csv_out, delimiter=" ")
                                for r in out_reader:
                                    u_x=float(r[8])
                                    u_y=float(r[9])
                                    U=math.sqrt(u_x*u_x+u_y*u_y)
                                    sum=sum+U
                            U_final=float(sum/eleven)
                            x_center=((x_first+x_second_last)/2)
                            y_center=((y_first+y_second_last)/2)
                            R=math.sqrt((x_center+0.5)**2)
                            L=math.sqrt((x_second_last-x_first)**2+(y_second_last-y_first)**2)
                            mass=2*3.142*R*L*U_final
                            with open(final, "a") as final:
                                final.write(f"{t2} {mass} \n")
                        else:
                            pass
                                
                        


