from tempfile import NamedTemporaryFile as namedTmp
import sys
import subprocess as sp

dbFile = sys.argv[1]
bedFile = sys.argv[2]
tables = ["feature","evidence","feature_evidence"]







def createDBFiles(table):
    cmd = "sqlite3 -csv {0} \" SELECT * FROM {1};\" > /tmp/{1}.csv".format(dbFile,table)
    sp.call(cmd, shell=True)

[createDBFiles(x) for x in tables]
