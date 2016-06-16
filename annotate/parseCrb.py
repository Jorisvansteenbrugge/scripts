from sys import argv

blastResult = argv[1]
bedFile = argv[2]
codeTable = argv[3]
finalDic = {}
codes = {}



for i in open(codeTable):
    line = i.strip().split("\t")
    codes[line[0]] = line[2]
    
with open(blastResult) as blast:
    for i in blast:
        line = i.strip().split("\t")
        line[0] = line[0].replace("(-)","")
        line[0]= line[0].replace("(+)","")
        

        try:
            term = "".join(line[1].split(".")[0:2])
            ID = codes[term]
            print(ID)
            finalDic[line[0].replace(":","").replace("-","")] = ID
        except KeyError:
            pass



with open(bedFile) as bed:
    for i in bed:
        line = i.strip().split("\t")
        pos = line[0]+line[1]+line[2]
        try:
            line[3] = finalDic[pos]
        except KeyError:
            pass
        #print("\t".join(line))


    



   
