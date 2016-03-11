#!/usr/bin/env python

import yaml
import re
import glob
import os

datalist=[]
annolist=[]



def createObjects():
    global datalist
    global annolist

    ask = True
    while ask:
        entryType = raw_input("Annotation or Data entry (a/d) ")
        entry = {}
        entry["name"] = raw_input("Name: ")
        entry["path"] = getFiles(raw_input("Path: "))
        if entryType =='d':
            feature = raw_input("Data feature (first/rpkm/etc.): ")
            if raw_input("chipseq? (y/n) :") == 'y':
                entry["up"] = 1000
                entry["down"] = 1000

            datalist.append(entry)
        else:
            entry["type"] = raw_input("Type: ")
            annolist.append(entry)
        ask = contin()
        print(entry)

def getFiles(path):
    m = re.search(r'\.[a-z]{3}$', path)
    if m: #anno entry
        return path
    else: #data entry
        return parseFolder(path)

def parseFolder(path):
    os.chdir(path)
    files = []
    for file in glob.glob("*.bam"):
        files.append(file)
    return files

def contin():
    answ = raw_input("Another entry? (y/n) ")
    if answ == 'y':
        return True
    else:
        return False

def writeObjects():
    print("annotation:\n")
    print(yaml.dump(annolist, default_flow_style=False))
    print("\ndata:\n")
    print(yaml.dump(datalist, default_flow_style=False))

def main():
    createObjects()
    writeObjects()

main()
