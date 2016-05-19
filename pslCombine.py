#!/usr/bin/env python
#author Joris van Steenbrugge
#since March 11
#Function: Combines multiple psl files into a single one
import sys

HEADER = open("blatHeader.psl")
for i in HEADER:
	print(i)


LEN = len(sys.argv) - 1
for i in range(0,LEN,1):
	count = 1
	fname = sys.argv[i+1]
	file = open(fname)
	for line in file:
		if count > 5:
			print(line)

		count +=1

	print(count)
