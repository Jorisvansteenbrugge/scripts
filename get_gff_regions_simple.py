#!/usr/bin/env python

from sys import argv, exit


if len(argv) <= 2:
    exit("usage: ./get_gff_regions_simple.py <regions.gff> {id1, id2, id3, ..., idn}")


if __name__ == "__main__":
    with open(argv[1]) as gff_file:
        for line in gff_file:
            if line.startswith('#'):
                continue

            line = line.strip().split('\t')

            if line[2] != 'mRNA':
                continue
            
            att_part = line[8]
            transcript_id = att_part.split(';')[0].replace("ID=","")
            
            if transcript_id in argv[2:]:
                print(f"{line[0]}\t{line[3]}\t{line[4]}\t{transcript_id}\t0\t{line[6]}")
