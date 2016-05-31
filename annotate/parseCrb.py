from pybedtools import BedTool
from sys import argv

blastResult = argv[1]
bedFile = argv[2]

dic = {}

with open(blastResult) as blast:
    for i in blast:
        line = i.strip().split("\t")
        line[0] = line[0].replace("(-)","")
        line[0]= line[0].replace("(+)","")

        dic[line[0].replace(":","").replace("-","")] = line[1]


with open(bedFile) as bed:
    for i in bed:
        line = i.strip().split("\t")
        pos = line[0]+line[1]+line[2]
        try:
            line[3] = dic[pos]
        except KeyError:
            pass
        print("\t".join(line))


    



    
