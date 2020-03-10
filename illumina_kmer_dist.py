#!/usr/bin/env python
from sys import argv
from Bio import SeqIO

k_dict = {}

def to_kmers(seq, k_size = 23):
    for i in range(len(seq)):
        kmer = seq[i:(i+k_size)]
        if len(kmer) < k_size:
            continue

        yield kmer

def output_kdict(k_dict):
    for key in k_dict:
        val = k_dict[key]
        print(f'{key}\t{val}')

if __name__ == "__main__":
    for seq_record in SeqIO.parse(argv[1], 'fastq'):
        sequence = str(seq_record.seq)

        for kmer in to_kmers(sequence):

            if kmer in k_dict:
                k_dict[kmer] += 1
            else:
                k_dict[kmer] = 1


    output_kdict(k_dict)
