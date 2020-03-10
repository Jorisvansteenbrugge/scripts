#!/usr/bin/env python

from sys import argv

stage = argv[2]

with open(argv[1]) as kofile:
	for line in kofile:
		try:
			lines = line.strip().split(';')

			print(f"{stage}\t{lines[1]}\t{lines[2]}\t{lines[6]}")
		except IndexError:
			line = line.strip().split()
			print(f"{stage}\t{line[1]}\t{line[2]}\t{line[6]}")
