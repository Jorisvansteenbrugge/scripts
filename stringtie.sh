#!/bin/bash

for i in $1*.bam
do
	stringtie $i -p 4 -o $(basename $i .bam).gtf
done
