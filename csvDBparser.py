from TemporaryFile import NamedTemporaryFile as namedTmp
import sys
import subprocess as sp

dbFile = sys.argv[1]
tables = ["feature","evidence","feature_evidence"]

[createDBFiles(x) for x in tables]




def createDBFiles(table):
    cmd = "sqlite3 -header -csv {0} \" SELECT * FROM {1};\" > /tmp/{1}.csv".format(dbFile,table)
    sp.call(cmd, shell=True)
