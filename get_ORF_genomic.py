from Bio import SeqIO
from subprocess import Popen, PIPE

orf_prot_file = "/home/joris/nemaNAS/steen176/Ava/data/genome_sequences/orfs/orfs_75_110/eloidogyne_incognita.PRJEB8714.WBPS14.genomic_softmasked.fa.orfs_75_110.fa"
genome_file = "/home/joris/nemaNAS/steen176/Ava/data/genome_sequences/meloidogyne_incognita.PRJEB8714.WBPS14.genomic_softmasked.fa"

for record in SeqIO.parse(orf_prot_file, 'fasta'):
	header = record.description.split(' ')

	chrom = header[0].split('_')[0]
	start = header[1].replace("[",'')
	end = header[3].replace("]",'')


	if (int(start) < int(end)):
		region_fmt = f"{chrom}:{start}-{end}"
	else:
		region_fmt = f"{chrom}:{end}-{start}"	

	p = Popen(f'samtools faidx {genome_file} {region_fmt}', shell = True)

	

