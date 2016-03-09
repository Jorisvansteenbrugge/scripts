#!/bin/bash

for i in $1*.bam
do
	echo $i
	stringtie $i -p 4 -G /home/jsteenbrugge/data/misc/Xtropicalisv9.0.Named.primaryTrs.gff3 -o $(basename $i .bam).gtf
done

