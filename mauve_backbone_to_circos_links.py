#!/usr/bin/env python3

import argparse
from itertools import combinations
from sys import exit, stdout



class Genome:
    def __init__(self, name, coords, presence):
        self.name     = name
        self.start    = coords[0]
        self.stop     = coords[1]
        self.presence = presence

    def __str__(self):
        return self.__repr__()

    def __contains__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name


iso_file = 0

def get_args():
    p = argparse.ArgumentParser(epilog="currently reverse strand alignments are ignored for simplicity")

    p.add_argument('-i', help='input alignment.backbone file (from Mauve output)', 
                   required = True, dest = 'backbone')
    p.add_argument("--threshold", help ='block length threshold (removes small alignments)',
                   required = False, dest = 'threshold', type = int)
    p.add_argument('--isolate', help = 'You can define a genome to isolate',
                   required = False, dest = 'isolate')
    p.add_argument("--isolate-output", help = 'output file for the features without the isolated genome',
                   required = False, dest = 'isooutput')

    return p.parse_args()


def has_seq(coord):
    return coord[0] != coord[1] and not coord[0].startswith('-')

def get_coords(line, x):
    return line[x], line[x + 1]

def is_isolate_in_genomes(genomes, isolate):
    genome_names = [x.name for x in genomes]
    return isolate in genome_names 

def is_coord_long_enough(coord, len_threshold):
    length = abs(abs(int(coord[0])) - abs(int(coord[1])))

    if length >= len_threshold:
        return True
    else:
        return False



def output(combis, len_threshold, out_source = stdout):
    
    for combination in combis: 
        A, B = combination

        if not is_coord_long_enough((A.start, A.stop), len_threshold):
            continue
        else:

            out = f"{A.name} {A.start} {A.stop} {B.name} {B.start} {B.stop}"
            print(out, file = out_source)

def parse_backbone(backbone, len_threshold, isolate = None ):
    with open(backbone) as bb:
        header = bb.readline().strip().split('\t')

        n_col = len(header)
        n_sample = n_col / 2
        sample_names = [header[x].split("_")[0] for x in range(0, n_col, 2)]

        for line in bb:
            line = line.strip().split('\t')

            coords = [ get_coords(line, x) for x in range(0, n_col, 2) ]

            presence = [has_seq(coord) for coord in coords]

            genomes = []
            for i in range(len(coords)):
                if not presence[i]:
                    continue

                genomes.append(Genome(sample_names[i], coords[i], presence[i]))
            if len(genomes) < 2:
                continue

            combis = combinations(genomes,2)
            iso_status = isolate != None


            if iso_status:
                if is_isolate_in_genomes(genomes, args.isolate):
                    # normal print
                    output(combis, len_threshold)
                else:
                    output(combis, len_threshold, iso_file)
            else:
                output(combis, len_threshold)

def open_iso_file(args):
    global iso_file

    iso_file = open(args.isooutput, 'w')
            


if __name__ == "__main__":
    args = get_args()

    if args.isolate and not args.isooutput:
        print("if you define an isolate you also have to define an isolate output file")
        exit(1)

    if args.isolate:
        open_iso_file(args)
        parse_backbone(args.backbone, args.threshold, args.isolate)
    else:
        parse_backbone(args.backbone, args.threshold)

