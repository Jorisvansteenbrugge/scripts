#!/usr/bin/env python

from Bio import SeqIO
from sys import argv
from tempfile import NamedTemporaryFile as namedTemp
import subprocess as sp
import argparse




def parseFasta(fastaF,outF, bed):
    outfile = open(outF,"w")
    fasta_seqs = SeqIO.parse(open(fastaF),"fasta")
    count = 0
    print("fasta parse")
    for fasta in fasta_seqs:
        query = namedTemp(delete=False)
        print("fasta found")
        if count < 2:
            name, seq = fasta.id, str(fasta.seq)
            seqout = ">{}\n{}\n".format(name,seq)
            print(seqout)
            print(query.name)
            query.write(seqout)
            query.flush()
            
            #calling the blastp program. Resulting in the file with the blast results
            resultFile = annotateSeq(query.name)
            
            print("result file")
            pos, refID = getBestResult(resultFile)
            if refID != "":
                outfile.write("\t".join(improveBed(pos,refID, bed))+"\n")
                print("Something happened")
            else:
                print("Passed")
        else:
            return True
        count+=1
        query.close()

def annotateSeq(queryFile):
    resultFile = namedTemp(delete=False)
    CMD = "blastp -db nr -query {} -out {} -remote".format(queryFile, resultFile.name)
    sp.call(CMD,shell=True)
    print(resultFile.name)
    return resultFile.name

def improveBed(pos, refID,bed):
    print("improve")
    bedPos = pos.replace(":","\t")
    bedPos = bedPos.replace("-","\t")
    bedPos = bedPos.replace("_","")

    interFile = namedTemp()
    interFile.write(bedPos+"\n")
    interFile.flush()

    CMD = "bedtools intersect -a {} -b {}".format(bed,interFile.name)
    handle = sp.Popen(CMD,shell=True,stdout=sp.PIPE)
    line = handle.stdout.readline().strip()
    line = line.split("\t")

        
    line[3] = refID
    return line

def getBestResult(resultFile):
    print("best result")
    pos = ""
    refID = ""
    with open(resultFile) as inf:
        for line in inf:
            if "Query=" in line and pos=="":
                pos = line.split("= ")[1].strip()
            elif "ref|" in line and "XP_" not in line:
                refID = line.split("|")[1]
            elif "gb|" in line:
                refID = line.split("|")[1]
            if pos != "" and refID != "":
                return pos, refID

    
def parseArgs():
    p = argparse.ArgumentParser()
    p.add_argument("-p", dest="prot", help="Fasta file with protein sequences", required=True)
    p.add_argument("-b", dest="bed", help="Bed file with existing genome annotations", required=True)
    p.add_argument("-o", dest="output", help="Output bed file", required=True)
    return p.parse_args()


if __name__ == "__main__":
    args = parseArgs()
    if parseFasta(args.prot, args.output, args.bed):
        print("1000 records parsed")
    
