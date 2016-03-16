from distutils.core import setup
import sys

VERSION = "0.1"
DESCRIPTION="Scripts"


setup (name="scripts",
	version = VERSION,
	description = DESCRIPTION,
	author = "Joris van Steenbrugge",
	author_email="jorisvsteenbrugge@gmail.com",
	license='MIT',
	url = "https://github.com/jorisvansteenbrugge/scripts",
	packages=[
		'scripts'
	],
	scripts=[
		"bam2default",
		"autoVirtEnvMaker",
		"depr_yamlMaker",
		"fastaSplitter",
		"fastq2bw",
		"getChrSizes",
		"multiBlat.sh",
		"pslCombine.py",
		"rna2bw",
		"sc",
		"spliceGetter",
		"sra_process.sh",
		"stringtie.sh",
		"wigToBigWig",
		"yamlMaker",
		"validation/peakStart",
	],
)

