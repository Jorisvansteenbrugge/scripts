#/usr/bin/env python

from Bio import SeqIO
from sys import argv

for record in SeqIO.parse(argv[1], 'fasta'):
	if record.id in argv[3:]:
		print(f">{argv[2]}_{record.id}\n{str(record.seq)}")