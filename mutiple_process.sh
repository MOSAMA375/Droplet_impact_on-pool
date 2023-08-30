#!/bin/bash

for ((i = 0; i < 1; i++)); do
  for ((j = 0; j <= 1; j++)); do
    for ((k = 0; k <= 9; k+=2)); do
      for ((l = 0; l < 1; l++)); do
        t=${i}.${j}${k}${l}
        FILE=i-${i}.${j}${k}${l}.gnu
        if [ -f "$FILE" ]; then
          mkdir Jet$t
          cp i-$t.gnu Jet$t/i-$t.gnu
          cp jet_cut.sh Jet$t/jet_cut.sh
          chmod +x Jet$t/jet_cut.sh
          (
            cd Jet$t
            nohup ./jet_cut.sh &
          )
        fi
      done
    done
  done
done
