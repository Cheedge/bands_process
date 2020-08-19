#!/bin/bash
#2020-08-18 12:29
for AtomSp in Mo W
do
	paste ${AtomSp}-1.dat ${AtomSp}-2.dat ${AtomSp}-3.dat ${AtomSp}-4.dat ${AtomSp}1.dat ${AtomSp}2.dat ${AtomSp}3.dat ${AtomSp}4.dat > temp
	awk '{printf "%lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf   %lf  %lf   %lf\n", $1, $2, $3-$4, $6, $7-$8, $10, $11-$12, $14, $15-$16, $18, $19-$20, $22, $23-$24, $26, $27-$28, $30, $31-$32}' temp > ${AtomSp}_new.dat 
	rm temp
done
