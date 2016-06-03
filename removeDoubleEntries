#!/usr/bin/env python
from Bio import SeqIO
import sys

outfile = open(sys.argv[2],"w")
check = {}

fasta_seqs = SeqIO.parse(open(sys.argv[1]),"fasta")

for fasta in fasta_seqs:
    name, seq = fasta.id, str(fasta.seq)
    check[name] = seq


with open(sys.argv[2], "w") as outFile:
    for entry in check.keys():
        outFile.write(">{}\n{}\n".format(entry,check[entry]))

outFile.close()
