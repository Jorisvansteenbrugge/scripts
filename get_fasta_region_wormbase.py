#!/usr/bin/env python3
from Bio import SeqIO
from sys import argv, exit



def get_wb_dict(ids):
    dic = {}
    for id in ids:
        wbid,group = id.split('_')
        dic[wbid] = id

    return dic

if __name__ == "__main__":
    if len(argv) <= 1:
        exit("usage script.py file.fasta {idA, idB, ...., idN}")

    worm_ids = get_wb_dict(argv[2:])
    
    for worm_id in worm_ids.keys():
        for record in SeqIO.parse(argv[1], 'fasta'):
            if worm_id in record.description:
                print(f">{worm_ids[worm_id]} \n{str(record.seq)}")
                break
