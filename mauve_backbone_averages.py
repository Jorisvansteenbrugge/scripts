#!/usr/bin/env python
from sys import argv
from statistics import mean

l19 = []
l22 = []
ro1 = []

l19_new = []
l22_new = []

with open(argv[1]) as backbone_file:
	header = backbone_file.readline()

	for line in backbone_file:
		line  = [abs(int(x)) for x in line.strip().split()]
		l22_s = line[0]
		l22_e = line[1]

		l19_s = line[2]
		l19_e = line[3]

		ro1_s = line[4]
		ro1_e = line[5]

		if 0 not in line:
			l19.append(l19_e-l19_s)
			l22.append(l22_e-l22_s)
			ro1.append(ro1_e-ro1_s)

		elif ro1_s == 0 and ro1_e == 0:
			l19_new.append(l19_e-l19_s)
			l22_new.append(l22_e-l22_s)


print(f"Ro1 avg region: {mean(ro1)}")
print(f"L22 avg region: {mean(l22)}")
print(f"L19 avg region: {mean(l19)}")


print(f"L22new avg region: {mean(l22_new)}")
print(f"L19new avg region: {mean(l19_new)}")

