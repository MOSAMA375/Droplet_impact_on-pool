#!/bin/bash
tmp=$(mktemp -d)

rm -r Angle
mkdir -p Angle

for ((i = 0; i <= 9; i++)); do
  for ((j = 0; j <= 9; j++)); do
    for ((k = 0; k <= 9; k++)); do
      for ((l = 0; l <= 9; l++)); do
        t=${i}.${j}${k}${l}
        FILE="i-${i}.${j}${k}${l}.gnu"
        if [ -f "$FILE" ]; then
          awk '$1 >= -0.43 && $2 >= -0.441 {print $1, $2}' "$FILE" >"$tmp/out"
          X_max=$(awk 'BEGIN {max = -100} {if ($1 > max) {max = $1}; } END {print max}' "$tmp/out")
          awk -v x_max="$X_max" '$1 == x_max {print $2}' "$tmp/out" >"$tmp/out2"
          Y_req=$(awk 'NR==1 {print; exit}' "$tmp/out2")
          line_num=$(awk -v x_max="$X_max" -v y_req="$Y_req" '$1 == x_max && $2 == y_req {print NR; exit}' "$FILE")
          num_lines=$(wc -l < "$FILE")

          awk -v line_num="$line_num" 'NR >= line_num && $1 > -0.43 {print $1, $2}' "$FILE" >"$tmp/out3"
          Y_min=$(awk 'NR==1 {min = 100} $2 < min {min = $2} END {print min}' "$tmp/out3")
          awk -v y_min="$Y_min" '$2 == y_min {print $1}' "$tmp/out3" >"$tmp/out4"
          X_req=$(awk 'NR==1 {print; exit}' "$tmp/out4")
          line_num1=$(awk -v y_min="$Y_min" -v x_req="$X_req" '$1 == x_req && $2 == y_min {print NR; exit}' "$FILE")

          awk -v line_num1="$line_num1" -v line_num="$line_num" 'NR >= line_num && NR <= line_num1 {print $1, $2}' "$FILE" > "$tmp/out5"
          Y_max=$(awk 'BEGIN {max = -100} $2 > max {max = $2} END {print max}' "$tmp/out5")
          awk -v y_max="$Y_max" '$2 == y_max {print $1}' "$tmp/out5" >"$tmp/out6"
          X_ymax=$(awk 'NR==1 {print; exit}' "$tmp/out6")
          line_num2=$(awk -v y_max="$Y_max" -v x_ymax="$X_ymax" '$1 == x_ymax && $2 == y_max {print NR; exit}' "$FILE")

          y1=$(awk "BEGIN {print $Y_min+(($Y_max - $Y_min)/2)}")
          Y_mid=$(awk -v y1="$y1" 'BEGIN {min = 100} {diff = y1 - $2; if (diff < 0) diff = -diff; if (diff < min) { min = diff; Y_mid = $2 }} END {print Y_mid}' "$tmp/out5")
          awk -v y_mid="$Y_mid" '$2 == y_mid {print $1}' "$tmp/out5" >"$tmp/out7"
          X_mid=$(awk 'NR==1 {print; exit}' "$tmp/out7")

          # Calculate the slope of the tangent line
          tangent_slope=$(awk -v x_mid="$X_mid" -v y_mid="$Y_mid" \
                           '$1 == x_mid && $2 == y_mid {getline; x1=$1; y1=$2; getline; x2=$1; y2=$2; print (y2-y1)/(x2-x1)}' "$tmp/out5")

          # Calculate the y-intercept of the tangent line
          tangent_intercept=$(awk -v x_mid="$X_mid" -v y_mid="$Y_mid" -v slope="$tangent_slope" \
                               '$1 == x_mid && $2 == y_mid {y_int = $2 - slope * $1; print y_int}' "$tmp/out5")

          # Calculate the x-coordinate of the point of intersection
          x_intersection="$X_mid"

          # Calculate the y-coordinate of the point of intersection using the tangent line equation
          y_intersection=$(echo "$tangent_slope * $x_intersection + $tangent_intercept" | bc -l)

          # Calculate the x-coordinate of the vertical line passing through (X_req, Y_min)
          x_vertical="$X_req"

          # Calculate the y-coordinate of the vertical line passing through (X_req, Y_min)
          y_vertical=$(echo "$tangent_slope * $x_vertical + $tangent_intercept" | bc -l)

          # Append the coordinates of the vertical line to the "intersect" file
          echo "$x_vertical $y_vertical" >> "intersect"

          d1=$(awk "BEGIN {print $Y_mid - $y_vertical}")
          d2=$(awk "BEGIN {print $X_mid - $X_req}")

          theta=$(awk "BEGIN {print atan2($d2, $d1)}")

          echo "$t $X_mid $Y_mid $theta"  
          echo "$t $X_mid $Y_mid $theta" >> "Angle/curvature.dat"
        fi
      done
    done
  done
done

# Remove the temporary directory and its contents
rm -r "$tmp"

