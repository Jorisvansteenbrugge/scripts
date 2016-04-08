#!/usr/bin/env python
import sqlite3 as sql
import sys

dbFile = sys.argv[1]
range = 1000

class DB:
    cursor = None
    
    def __init__(self):
        con = None
        try:
            con = sql.connect(dbFile)
            self.cursor = con.cursor()
        except sql.Error:
            print("Cannot connect to {0}".format(dbFile))
            sys.exit(1)

    def search(self, line):
        if line != "":
            chrom = line[0]
            start = line[1]
            end = line[2]
            strand = line[5]

            statement = "SELECT id FROM feature WHERE chrom='{0}' AND start BETWEEN'{1}' AND '{2}' AND end BETWEEN '{3}' AND '{4}' AND strand='{5}'".format(chrom,int(start)-range,int(start)+range,int(end)-range, int(end)+range, strand)
            self.cursor.execute(statement)

            rows = self.cursor.fetchall()
            id = rows[0][0]
            return self.getName(id)
            
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
            line[3] = database.search(line)
        except IndexError:
            pass
        print("\t".join(line))
         

        
