#!/bin/bash
tmp=$(mktemp -d)

poolh=-0.46

for ((i = 0; i <= 9; i++)); do
  for ((j = 0; j <= 9; j++)); do
    for ((k = 0; k <= 9; k++)); do
      for ((l = 0; l <= 9; l++)); do
        for ((m = 0; m <= 9; m++)); do
         t=${i}.${j}${k}${l}${m}
          
         FILE1=i-${i}.${j}${k}${l}${m}.gnu

        if [ -f "$FILE1" ]; then
          awk '$1 >= -0.43 {print $1, $2 > "j-'"$t"'.gnu";}' "i-$t.gnu"
        fi
    
        FILE=j-${i}.${j}${k}${l}${m}.gnu
        if [ -f "$FILE" ]; then
          awk '$1 >= -0.43 && $2 >= -0.442  {print $1, $2}' "$FILE" >"$tmp/out"
          X_max=$(awk 'BEGIN {max = -100} {if ($1 > max) {max = $1}; } END {print max}' "$tmp/out")
          awk -v x_max="$X_max" '$1 == x_max {print $2}' "$tmp/out" >"$tmp/out2"
          Y_req=$(awk 'NR==1 {print; exit}' "$tmp/out2")
          line_num=$(awk -v x_max="$X_max" -v y_req="$Y_req" '$1 == x_max && $2 == y_req {print NR; exit}' "$FILE")
          num_lines=$(wc -l < "$FILE")
          
          awk -v line_num="$line_num" 'NR >= line_num && $1 > -0.43 {print $1, $2}' "$FILE" >"$tmp/out3"
          Y_min=$(awk 'NR==1 {min = $2} $2 < min {min = $2} END {print min}' "$tmp/out3")
          awk -v y_min="$Y_min" '$2 == y_min {print $1}' "$tmp/out3" >"$tmp/out4"
          X_req=$(awk 'NR==1 {print; exit}' "$tmp/out4")
          line_num1=$(awk -v x_req="$X_req" -v y_min="$Y_min" '$1 == x_req && $2 == y_min {print NR; exit}' "$FILE")

          if python -c "import sys; sys.exit(1 if float('$Y_min') <= float('$poolh') else 0)"; then
            dangle=0.1
            tmp="tmp_folder"  # Replace with the actual temporary folder path

            # Create the temporary folder if it doesn't exist
            mkdir -p "$tmp"

            # Extract xL and yL values from the input file
            awk -v line_num="$line_num" '
                NR >= 1 && NR <= line_num {
                    xL[NR] = $1;
                    yL[NR] = $2;
                }
                END {
                    print "declare -a xL=(";
                    for (i=1; i<=NR; i++) {
                        printf "\"%s\"", xL[i];
                        if (i < NR) {
                            printf " ";
                        }
                    }
                    print ")";
                    print "declare -a yL=(";
                    for (i=1; i<=NR; i++) {
                        printf "\"%s\"", yL[i];
                        if (i < NR) {
                            printf " ";
                        }
                    }
                    print ")";
                }
            ' "$FILE" > "$tmp/out5"

            source "$tmp/out5"

            # Calculate the rotated points
            angle=$(echo "scale=8; (3.1415/1000) + 270 - $dangle" | bc)
            c=$(echo "$angle" | awk '{print cos($1)}')
            s=$(echo "$angle" | awk '{print sin($1)}')
            v_x_arr=()
            v_y_arr=()

            for ((i = 1; i <= ${#xL[@]}; i++)); do
                u_x=$(awk -v xL="${xL[i]}" -v X_req="$X_req" 'BEGIN {print xL - X_req}')
                u_y=$(awk -v yL="${yL[i]}" -v Y_min="$Y_min" 'BEGIN {print yL - Y_min}')
                v_x=$(awk -v u_x="$u_x" -v u_y="$u_y" -v c="$c" -v s="$s" 'BEGIN {print u_x * c + u_y * s}')
                v_y=$(awk -v u_x="$u_x" -v u_y="$u_y" -v c="$c" -v s="$s" 'BEGIN {print u_y * c - u_x * s}')
                v_x_arr+=($v_x)
                v_y_arr+=($v_y)

                echo "${v_x} ${v_y}" >> rotated_points.dat
                echo "${xL[i]} ${yL[i]}" >> original_points.dat
            done

            min_idx=0
            min_dist=${v_y_arr[0]}
            for ((i = 1; i < ${#v_y_arr[@]}; i++)); do
                if (( $(echo "${v_y_arr[i]} < $min_dist" | bc -l) )); then
                    min_dist=${v_y_arr[i]}
                    min_idx=$i
                fi
            done

            xtang=${xL[min_idx]}
            ytang=${yL[min_idx]}

            xtang_line=$(awk -v x_tan="$xtang" -v y_tan="$ytang" '$1 == x_tan && $2 == y_tan {print NR; exit}' "$FILE")

            echo "$t $X_max $Y_req $X_req $Y_min $xtang $ytang" >> curvature.dat
            rm rotated_points.dat original_points.dat  
            awk -v xtang_line="$xtang_line" -v line_num1="$line_num1" 'NR >= xtang_line && NR <= line_num1 {print $1, $2}' "$FILE" > "nj-$t.gnu"

          else
            awk -v line_num1="$line_num1" 'NR >= 1 && NR <= line_num1 {print $1, $2}' "$FILE" > "nj-$t.gnu"
    
          fi

          jet_file="nj-$t.gnu"
          first_line=$(head -n 1 "$jet_file")
          echo "$first_line" >> "$jet_file"
          
          rm "j-$t.gnu"
          rm -r "$tmp"
          
        fi
      done
    done
  done
 done
done

