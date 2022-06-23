#!/bin/bash

( 
for (( i=0; i<1; i++ )); do
for (( j=0; j<=9; j++ )); do
for (( k=0; k<=9; k++ )); do
for (( l=0; l<=9; l++ )); do
for (( m=0; m<=9; m++ )); do

FILE=snapshot-${i}.${i}${j}${k}${l}${m}.gfs
if [ -f "$FILE" ]; then
cat  snapshot-${i}.${i}${j}${k}${l}${m}.gfs


echo "Save filament-${i}${j}${k}${l}${m}.ppm {format = PPM orientation = Portrait line_width = 1 width = 1920 height = 1080 sort = Simple}"

fi
done
done
done
done
done
) | gfsview-batch2D view.gfv

cat *.ppm | ppm2mpeg > filament_20_1.mpg

#echo "EventScript { istep=1 } { echo "Save t-${i}.${i}${j}${k}${l}${m}.eps { format = EPS }" }"
