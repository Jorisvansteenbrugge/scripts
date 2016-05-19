#!/bin/bash
#Author: simon van heeringen
#Function: Calculates the occurences of splice sites in bed3 format and give a count 
if [ $1 ]; then
	cat $1  | uniq -c | perl -ple 's/^\s*(\d+)\s+(.+)/$2\t$1/'
fi
