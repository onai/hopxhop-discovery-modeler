#!/bin/bash


for d in 5 10 20 100 200
do
    for N in 5 10 15 20 50 100 200 500 5000
    do
        for ds in 2 3 4 5 10 15 20 50
        do
            for n in 2 3 4 5 10 15 20
            do
                if [ $d -le $N  -a $ds -le $N -a $n -le $N ]; then

                    echo "config: d: $d, N: $N, ds: $ds, de: $(( $ds + 3 )), n: $n" >> flooding.txt
                    for i in `seq 1 100`;
                    do
                        python3 flooding_every.py $d $N $ds $(($ds + 3)) $n >> flooding.txt;
                    done
                fi
            done
        done
    done
done
