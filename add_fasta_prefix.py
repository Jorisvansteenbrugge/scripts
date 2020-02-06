#!/usr/bin/env python

from sys import argv
from Bio import SeqIO
prefix = argv[2]

for record in SeqIO.parse(argv[1], 'fasta'):
    seq_id = record.id
    seq = str(record.seq)

    print(f">{prefix}{seq_id}\n{seq}")


