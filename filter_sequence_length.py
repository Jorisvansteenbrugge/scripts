#!/usr/bin/env python


from sys import argv
from Bio import SeqIO


def check_length(seq, minLen = 75, maxLen = 110):
	seq_len = len(str(seq))
	return True if  seq_len > minLen and len(str(seq)) <= maxLen else False
	

if __name__ == '__main__':
	for record in SeqIO.parse(argv[1], 'fasta'):
		if check_length(record.seq):
			print(f">{record.description}\n{record.seq}")

