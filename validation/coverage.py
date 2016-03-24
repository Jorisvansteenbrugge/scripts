import os
from math import log
import sys
import pandas as pd
import glob
import subprocess as sp

identifier = "xXxcoveragexXx.bed"
rpkmFiles = []

def getCoverage(files,bamdir):
	for i in files:
                print(i)
		outfiles = parseBam(i,bamdir)
                coverageFile = mergeCounts(i,outfiles)
                avgFile,totalReads = getAvgCoverage(coverageFile)
                getRPKM(totalReads, avgFile)
                cleanUp(outfiles)
        plotFrame = paste()
	return plotFrame

def parseBam(bed, bamdir):
	os.chdir(bamdir)
        outfiles = []
	for file in ["H3K4me3_stage9_2.bam"]: #glob.glob("*.bam"):
                outfile = file.split(".bam")[0]+identifier
                outfiles.append(bamdir+outfile)
		cmd = "bedtools coverage -abam {0} -b {1}  -counts -d | cut -f 4 > {2}".format(file,bed,outfile)
		sp.call(cmd, shell=True)
        return outfiles

def mergeCounts(bed, outfiles):

	#take first collumn of bed
        outname = bed.split(".bed")[0]+"_regions.bed"
        regionsCMD = "cat {0} | cut -f 1-3 > {1}".format(bed, outname)
	sp.call(regionsCMD,shell=True)

        #pasta bamfiles
        finalOut = bed.split(".bed")[0]+".coverage"
        pasteCMD = "paste {0} {1} > {2}".format(outname, " ".join(outfiles), finalOut)
        sp.call(pasteCMD, shell=True)

        return finalOut

def getAvgCoverage(coverageFile):
        outname = coverageFile.split(".coverage")[0]+".avgCoverage"
        outfile = open(outname,"w")

        totalReads = 0
        with open(coverageFile) as file:
                for line in file:
                        line = line.strip().split("\t")
                        pos = line[0:3]
                        cov = line[3:]
			nums = []
                        for i,y in enumerate(cov):
                                try:
					nums.append(int(y))
				except:
					pass
			avg = None
                        try:
				avg = sum(nums)/len(nums)
			except:
				avg = 0
                        totalReads += avg
                        pos.append(str(avg))
                        outfile.write("\t".join(pos)+"\n")

        print("total reads for {0}: {1}".format(coverageFile,totalReads))
        outfile.close()
        return outname, totalReads

def getRPKM(totalReads, avgFile):
        outname = avgFile.split(".avgCoverage")[0]+".rpkm"
        outfile = open(outname,"w")
        rpkmFiles.append(outname)
        with open(avgFile) as file:
                outfile.write(os.path.basename(avgFile).split(".avgCoverage")[0]+"\n")
                for line in file:
			rpkm = 0
                        line = line.strip().split("\t")
                        length = int(line[2]) - int(line[1])
			try:
				cov = int(line[3])
				rpkm = (10e9*cov)/(totalReads*length)
			except:
				print(line)
                        outfile.write(str(rpkm)+"\n")

def paste():
        print("RPKM files: {0}".format(" ".join(rpkmFiles)))
        outfileName = "boxPlotData.tsv"
        output = open(outfileName,"w")
	output.write('\"Name\"\t\"RPKM log2\"\n')
	for i in rpkmFiles:
		input = open(i)
		first = input.readline().strip()
		for y in input:
			output.write('\"'+first+'\"'+"\t"+y)
	return pd.read_csv(outfileName, sep='\t')

def cleanUp(outfiles):
        clean = "rm {0}".format(" ".join(outfiles))
        sp.call(clean, shell=True)
