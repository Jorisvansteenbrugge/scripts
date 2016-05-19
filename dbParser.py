#!/usr/bin/env python
import sqlite3 as sql
import sys

dbFile = sys.argv[1]
boundary = 1000
class DB(object):
    cursor = None
    
    def __init__(self):
        con = None
        try:
            con = sql.connect(dbFile)
            self.cursor = con.cursor()
        except sql.Error:
            print("Cannot connect to {0}".format(dbFile))
            sys.exit(1)

    def search(self, chrom,start,end,strand):
        if line != "":
            chrom = line[0]
            start = line[1]
            end = line[2]
            strand = line[5]

            between = "SELECT id FROM feature WHERE chrom='{0}' AND start BETWEEN'{1}' AND '{2}' AND end BETWEEN '{3}' AND '{4}' AND strand='{5}'"
            between = between.format(chrom,int(start)-boundary,int(start)+boundary,int(end)-boundary, int(end)+boundary, strand)

            self.cursor.execute(between)

            rows = self.cursor.fetchall()
            return rows[0][0]
            #return self.getName(id)
            
    def getName(self,id):
        substatement = "SELECT evidence_id FROM feature_evidence WHERE feature_id='{0}'".format(id)
        statement = "SELECT name FROM evidence WHERE id IN ({0})".format(substatement)
        self.cursor.execute(statement)
        rows = self.cursor.fetchone()
        return rows[0].split(":::")[1]
    

bed = "/home/joris/Desktop/test.bed"
database = DB()

with open(bed) as f:
    for i in f:
        line = i.strip().split("\t")
        try:
            ids = []
            start = int(line[1])
            blSizes = line[10].split(",")
            blStarts = line[11].split(",")
            for x,y in enumerate(blSizes):
                try:
                    size = int(y)
                    chrom  = line[0]
                    st   = start+int(blStarts[x])
                    end  = st+size
                    ids.append(database.search(chrom,st,end,line[5]))
                except:
                    pass
            ids = list(set(ids))
            if len(ids) == 1:
                line[3] = database.getName(ids[0])
        except IndexError:
            pass
        print("\t".join(line))
