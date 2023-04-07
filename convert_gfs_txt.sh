#!/bin/bash

mkdir FILES

for (( i = 0; i < 1; i++ )); do
for (( j = 0; j <= 1; j++ )); do
for (( k = 0; k <=9; k+=2 )); do
for (( l = 0; l < 1; l++ )); do

t=${i}.${j}${k}${l}
echo ${i}.${j}${k}${l}

gerris2D -e "OutputSimulation {istep = 1} FILES/snapshot-${i}.${j}${k}${l}.txt {format=text variables = f,u_x,u_y,omega,p }" snapshot-${i}.${j}${k}${l}.gfs >a


done
done
done
done
