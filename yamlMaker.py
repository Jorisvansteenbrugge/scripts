#!/usr/bin/env python

#Author: Joris van Steenbrugge
#Date: februari 2016
#Function: Auto creates a yaml file with all the data files included for the pita pipeline to run

#Missing:
#	guided mode
import os
import sys
import argparse
import subprocess as sp
import glob
import yaml

data =[]
annotation=[]
scoring=[]
path=""

def parseArgs():
	global path
	p = argparse.ArgumentParser()
	p.add_argument("-methy", dest="h3k4me3", help="Directory with H3K4me3 bam files", required=False)
	p.add_argument("-rna", dest="rna", help="Directory with RNA-seq bam files", required=False)
	p.add_argument("-spl", dest="splice", help="Directory with splice site files", required=False)
	p.add_argument("-est", dest="est", help="EST file(s)", nargs="+", required=False)
	p.add_argument("-model", dest="model", help="Gene model file(s). This includes annotation files that don't fit in other categories", nargs="+", required=False)
	p.add_argument("-guided", dest="guided",help="Guided mode will enable you to add data folders at run-time without the use of additional flags. DEFAULT=False")
	p.add_argument("-o", dest="output",help="Output file (requires a full path for some reason)", required=True)

	args = p.parse_args()

	h3k4me3Dir = args.h3k4me3
	rnaDir = args.rna
	output = args.output
	splice = args.splice
	est= args.est
	model = args.model

	dirs = []


	#data entries
	if h3k4me3Dir:
		dirs.append(h3k4me3Dir)
	if rnaDir:
		dirs.append(rnaDir)
	if splice:
		dirs.append(splice)


	getPathconsensus(dirs)

	#annotation entries
	if est:
		for i,y in enumerate(est):
			est[i] = y.replace(path,"")
		addAnnotationEntry("EST",est)
	if model:
		for i,y in enumerate(model):
			model[i] = y.replace(path,"")

		addAnnotationEntry("GModel",model)

	if h3k4me3Dir:
		addDataEntry("H3K4me3",h3k4me3Dir,"start")
	if rnaDir:
		addDataEntry("RNAseq",rnaDir,"all")
	if splice:
		addDataEntry("RNAseq_splice" ,splice,"splice")

	return output

def addDataEntry(name, dir, feature):
	entry= {}
	type = raw_input("What is the filetype of "+name+"? ")
	fileList = getArray(dir, type)
	entry["name"] = name
	entry["path"] = fileList
	entry["type"] = type
	entry["feature"] = feature
	data.append(entry)
	addScoring(name,feature)

def addAnnotationEntry(name,fileList):
	entry ={}
	type = raw_input("What is the filetype of "+name+"? ")
	entry["name"] = name
	entry["path"]= fileList
	entry["type"] = type
	annotation.append(entry)

def addScoring(name, type):
	entry = {}
	entry["name"] = name
        entry["scoring"]= 1
        entry["type"] = type
	scoring.append(entry)

def getArray(dir, ext):
	global path
	os.chdir(dir)
	list = []
	[list.append(dir.replace(path,"")+file) for file in glob.glob("*."+ext)]
	return list

def writeFile(output):
	global path
	file = open(str(output),"w")
	file.write("data_path: "+path)
	file.write("\nAnnotation:\n")
	file.write(yaml.dump(annotation))
	file.write("\nData:\n")
	file.write(yaml.dump(data))
	file.write("\nscoring:\n")
	file.write(yaml.dump(scoring,default_flow_style=False))

def getPathconsensus(dirs):
	global path
	while len(dirs) >=2:
		v = commonStart(dirs[0],dirs[1])
		dirs[0] = v
		dirs.pop(1)
	path = dirs[0]

def stopIter():
    raise StopIteration

def commonStart(sa, sb):
	return ''.join(a if a == b else stopIter() for a, b in zip(sa, sb))

def printReminders():
	print("Don't forget to adjust the scoring weights to your preferences in the output file!")

if __name__ == "__main__":
	output = parseArgs()
	writeFile(output)
	printReminders()
