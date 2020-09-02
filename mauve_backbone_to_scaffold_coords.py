#!/usr/bin/env python

from sys import argv
from Bio import SeqIO


class Scaffold:

	def __init__(self, name, length, whole_genome_start):
		self.name = name
		self.length = length
		self.whole_genome_start = whole_genome_start
		self.whole_genome_end = (whole_genome_start+length)

	def __repr__(self):
		return f"<scaffold obj>: {self.name}"

	def get_real_scaffold_coordinate(self, whole_genome_region):
		reglen = whole_genome_region[1] - whole_genome_region[0]

		regstart = whole_genome_region[0] - self.whole_genome_start
		regend = regstart+reglen

		return f"{self.name}\t{regstart}\t{regend}"

genome = argv[1]
backbone = argv[2]
bb_start_col = int(argv[3])


def extract_scaffold_coords(genome):

	count_cursor = 1
	scaffolds_dict = {}

	for record in SeqIO.parse(genome, 'fasta'):
		seq = str(record.seq)
		current_scaffold = Scaffold(record.id, len(seq), count_cursor)

		count_cursor += len(seq)

		
		scaffolds_dict[current_scaffold.name] = current_scaffold

	return scaffolds_dict


def make_region_lookup_table(scaffolds):

	dic = {}

	for scaffold in scaffolds:
		for i in range(scaffold.whole_genome_start, scaffold.whole_genome_end, 1):
			dic[i] = scaffold.name

	return dic

def parse_mauve_backbone(backbone_file, start_col):
	with open(backbone_file) as bb:
		header = bb.readline()

		for line in bb:
			line = line.strip().split('\t')
			try:
				region = (line[start_col], line[(start_col+1)])
			except IndexError:
				print(line)
			region = [abs(int(pos)) for pos in region]

			yield region


scaffolds_dict = extract_scaffold_coords(genome)

region_dict = make_region_lookup_table(scaffolds_dict.values())


for bb_region in parse_mauve_backbone(backbone, bb_start_col):

    if bb_region[0] != 0:	
    	region_scaffold = region_dict[bb_region[0]]
    	scaffold = scaffolds_dict[region_scaffold]

    	print(scaffold.get_real_scaffold_coordinate(bb_region))
    else:
        print("NA\t0\t0")


