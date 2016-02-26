#!/usr/bin/env python
import os
import sys
import argparse
import subprocess as sp
import glob
import yaml



dict ={}
data =[]
annotation=[]
names

def parseArgs():
	p = argparse.ArgumentParser()
	p.add_argument("-methy", dest="h3k4me3", help="Directory with H3K4me3 bam files", required=False)
	p.add_argument("-rna", dest="rna", help="Directory with RNA-seq bam files", required=False)
	p.add_argument("-spl", dest="splice", help="Directory with splice site files", required=False)
	p.add_argument("-o", dest="output",help="Output file (requires a full path for some reason)", required=True)
	p.add_argument("-est", dest="est", help="EST directory", required=False)
	args = p.parse_args()

	h3k4me3Dir = args.h3k4me3
	rnaDir = args.rna
	output = args.output
	splice = args.splice
	est= args.est
	#annotation entries
	if est:
		addAnnotationEntry("EST",est)
	#data entries

	if h3k4me3Dir:
		addDataEntry("H3K4me3",h3k4me3Dir)
	if rnaDir:
		addDataEntry("RNAseq",rnaDir)
	if splice:
		addDataEntry("RNAseq_splice" ,splice)

	return output

def addDataEntry(name, dir):
	entry= {}
	type = raw_input("What is the filetype of "+name+"? ")
	fileList = getArray(dir, type)
	entry["name"] = name
	entry["path"] = fileList
	entry["type"] = type
	entry["feature"] = "all"
 	data.append(entry)


def addAnnotationEntry(name,dir):
	entry ={}
	type = raw_input("What is the filetype of "+name+"? ")
	fileList = getArray(dir,type)
	entry["name"] = name
	entry["path"]= fileList
	entry["type"] = type
	annotation.append(entry)

def getArray(dir, ext):
	os.chdir(dir)
	list = []
	[list.append(dir+file) for file in glob.glob("*."+ext)]
	return list



def writeFile(output):
	file = open(str(output),"w")
	file.write("Annotation :\n")
	file.write(yaml.dump(annotation))
	file.write("\nData :\n")
	file.write(yaml.dump(data))

if __name__ == "__main__":
	output = parseArgs()
	writeFile(output)
