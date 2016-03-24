import subprocess as sp
import sys

# intersectBed -wao -a bed1 -b bed2 > intersections
header = "gene\tstartA\tstartB\tstopA\tstopB\texon#A\texon#B\texonLenA\texonLenB\toverlap\texonSame"

def bleedingedge():
	bed1 = None
        bed2 = None
        try:
                bed1 = sys.argv[1]
                bed2 = sys.argv[2]
        except:
                print("Usage: python bedCompare bed1 bed2\n")
                sys.exit()

	
print("Chr\tstartA\tstopA\tnameA\tscoreA\tstrandA\tthickStartA\tthickEndA\trgbA\tblCountA\tblSizeA\blStartsA\t"+
	"startB\tstopB\tnameB\tscoreB\tstrandB\tthickStartB\tthickEndB\trgbB\tblCountB\tblSizeB\blStartsB\toverlap")
        intersectCMD = "intersectBed -wao -a {0} -b {1}".format(bed1,bed2)
        proc = sp.call(intersectCMD, shell=True)


def mainFlow():
	bed1 = None
	bed2 = None
	try:
		bed1 = sys.argv[1]
		bed2 = sys.argv[2]
	except:
		print("Usage: python bedCompare bed1 bed2\n")
		sys.exit()

	#bedTest = "Xtropicalisv9.0.Named.primaryTrs.names.bed"

	intersectCMD = "intersectBed -wao -a {0} -b {1}".format(bed1,bed2)
	proc = sp.Popen(intersectCMD, shell=True, stdout = sp.PIPE)

	print(header)
	for i in proc.stdout:
		outTable = []
		line = i.strip().split("\t")

		if line[24] != '0':
			outTable.append(line[3])               	# gene
			outTable.append(line[1])               	# startA
			outTable.append(line[13])              	# startB
			outTable.append(line[2])               	# stopA
			outTable.append(line[14])              	# stopB
			outTable.append(line[9])	       	# exon#A
			outTable.append(line[21])		# exon#B
			ex1 = getExonLength(line[10])
			ex2 = getExonLength(line[22])
			outTable.append(getExonLength(line[10])) #exonLenA
			outTable.append(getExonLength(line[22])) # exonLenB
			outTable.append(line[24])		# overlap
			if ex1 == ex2:
				outTable.append("1")
			else:
				outTable.append("0")
			print("\t".join(outTable))

def getExonLength(line):
	exonLen = 0
	for i in line.split(","):
		try:
			exonLen+=int(i.strip())
		except:
			pass #exclude
	return str(exonLen)


if __name__ == "__main__":
#	mainFlow()
	bleedingedge()
