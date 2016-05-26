#!/usr/bin/env python

from Bio import SeqIO
from tempfile import NamedTemporaryFile as namedTemp
import subprocess as sp
import argparse
import urllib



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

            intersectLine = checkIntersect(name, bed)
            
            if intersectLine != "":
                print("Interline: "+intersectLine)
                seqout = ">{}\n{}\n".format(name,seq)
                print(seqout)
                print(query.name)
                query.write(seqout)
                query.flush()

                #calling the blastp program. Resulting in the file with the blast results
                resultFile = annotateSeq(query.name)
            
                print("result file")
                refID = getProtID(resultFile)
                if refID != "" and refID != None:
                    geneSymbol = getGeneSymbol(refID)
                    outfile.write("\t".join(improveBed(geneSymbol, intersectLine))+"\n")
                    print("Something happened")
                else:
                    print("No ID found, Passed")
            else:
                print("No intersection found, skipping blast")
        else:
            return True
        count+=1
        query.close()

"""
Uses REST to convert refseq id's to geneSymbols
"""
def getGeneSymbol(refID):
    url = 'http://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?'
    url +='method=db2db&format=row&input=genesymbol&inputValues={0}&outputs=geneSymbol'.format(refID)
    u = urllib.urlopen(url)
    response = u.read()
    print(response)
    return response.split("<GeneSymbol>")[1].split("</GeneSymbol>")[0] #No fancy xml parsing going on here

def annotateSeq(queryFile):
    resultFile = namedTemp(delete=False)
    CMD = "blastp -db nr -query {} -out {}  -remote".format(queryFile, resultFile.name)
    sp.call(CMD,shell=True)
    print(resultFile.name)
    return resultFile.name

"""
Checks if the protein coordinates are present somewhere in the bed file. 
If not, the program skips the slow blast process.
"""
def checkIntersect(pos, bed):
    bedPos = pos.replace(":","\t")
    bedPos = bedPos.replace("-","\t")
    bedPos = bedPos.replace("_","")

    interFile = namedTemp()
    interFile.write(bedPos+"\n")
    interFile.flush()

    CMD = "bedtools intersect -a {} -b {}".format(bed,interFile.name)
    handle = sp.Popen(CMD,shell=True,stdout=sp.PIPE)
    line = handle.stdout.readline().strip()
    return line

def improveBed(geneSym, line):
    line = line.split("\t") 
    line[3] = geneSym
    return line

def getProtID(resultFile):
    print("best result")
    refID = ""
    with open(resultFile) as inf:
        for line in inf:
            if "ref|" in line:
                refID = line.split("|")[1]
            elif "gb|" in line:
                refID = line.split("|")[1]
            if refID != "":
                return refID

    
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
    
