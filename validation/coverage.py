import os
import sys
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
        paste()
        
def parseBam(bed, bamdir):
	os.chdir(bamdir)
        outfiles = []
	for file in glob.glob("*.bam"):
                outfile = file.split(".bam")[0]+identifier
                outfiles.append(bamdir+outfile)
		cmd = "bedtools coverage -abam {0} -b {1} -counts -d | cut -f 4 > {2}".format(file,bed,outfile)
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
                        for i,y in enumerate(cov):
                                cov[i] = int(y)
                        avg = sum(cov)/len(cov)
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
                        line = line.strip().split("\t")
                        length = int(line[2]) - int(line[1])
                        cov = int(line[3])
                        rpkm = (10e9*cov)/(totalReads*length)
                        outfile.write(str(rpkm)+"\n")

def paste():
        print("RPKM files: {0}".format(" ".join(rpkmFiles)))
        outfile = "~/boxPlotData.tsv"
        cmd = "paste {0} > {1}".format(" ".join(rpkmFiles), outfile)
        sp.call(cmd, shell=True)
        plot = "Rscript ~/tools/scripts/validation/boxPlotter.R {0} {1}".format(outfile, "~/boxplot.svg")
        sp.call(plot, shell= True)

def cleanUp(outfiles):
        clean = "rm {0}".format(" ".join(outfiles))
        sp.call(clean, shell=True)
    
if __name__ == "__main__":
	files =["/home/jsteenbrugge/gmodels1-3.bed", "/home/jsteenbrugge/pitaRun1-3.bed"]
	getCoverage(files, sys.argv[1])
