#!/usr/bin/env python

from sys import argv

start_col     = int(argv[2])
assembly_size = int(argv[3])

total_pos = 0
total_min = 0

uncovered = 0 # number of basepairs where there was no match with other genomes

with open(argv[1]) as backbone_file:
	header = backbone_file.readline()

	for line in backbone_file:
		line  = line.strip().split()

		start = int(line[start_col])
		end   = int(line[(start_col+1)])

		other_cols = list(range(len(line)))
		other_cols.pop(start_col)
		other_cols.pop(start_col)

		reg_size = abs(end) - abs(start)



		#if reg_size < 3000:
	#		continue

		


		if False in [line[col] == '0' for col in other_cols]:

			if start < 0 and end < 0:
				total_min += reg_size
			else:
				total_pos += reg_size

		else:
			uncovered += reg_size

		


		

total_covered    = sum([total_min,total_pos])
cov_percentage   = (total_covered/assembly_size) * 100

uncov_percentage = (uncovered/assembly_size) * 100

print(total_pos)
print(total_min)

print(f"Total all: {total_covered}, that is: {cov_percentage}% of the assembly size")
print(f"Total uncovered {uncovered}, that is: {uncov_percentage}% of the assembly_size")
