#!/bin/bash
#date='2020-08-17 23:21'

nBand=102
nKp=301
AtomSp=Se_W
for Name in BAND_S03_A0001 BAND_S03_A0002
do
	nlines=$[$nBand*$nKp+1]
	nlines300=$[$nlines+299]
	for i in 1 2 3 4
	do
		awk -v n0="${nlines}" -v n1="${nlines300}" '{if (NR>=n0 && NR<=n1) print $0;}' ${Name}.OUT > ${AtomSp}_$i.dat
		#sed -n ""${nlines}","${nlines300}" p" ${Name}.OUT > ${AtomSp}_$i.dat
		nlines=$[${nlines300}+2]
		nlines300=$[${nlines300}+301]
	done
	AtomSp=Se_Mo
done
