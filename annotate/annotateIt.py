#!/usr/bin/env python

from Bio import SeqIO
from sys import argv
from tempfile import NamedTemporaryFile as namedTemp
import subprocess as sp
import logging

logger = logging.getLogger("annotate")

def parseFasta():
    outfile = open(argv[2],"w")
    fasta_seqs = SeqIO.parse(open(argv[1]),"fasta")
    count = 0

    for fasta in fasta_seqs:
        query = namedTemp(suffix=".fa")
        if count < 2:
            name, seq = fasta.id, str(fasta.seq)
            query.write(">{}\n{}".format(name,seq))
            query.flush()
            logger.info("Blasting {}".format(name))
            newName = annotateSeq(query.name)
            logger.info("Old: {}  -- New: {}".format(name, newName))
        else:
            return True
        count+=1
        query.close()

def annotateSeq(queryFile):
    resultFile = namedTemp()
    CMD = "blastn -db nt -query {} -out {} -remote".format(queryFile, resultFile.name)
    sp.call(CMD,shell=True)
    
    



if __name__ == "__main__":
    if parseFasta():
        print("1000 records parsed")
    
