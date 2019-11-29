#!/usr/bin/env python3

from Bio import SeqIO
from subprocess import Popen, PIPE
from sys import argv

# De bekende files..
GENOME_22="/home/joris/nemaNAS/steen176/Annotation/G_ros22/G_rostochiensis_22_v0.8.fasta"
PROTEOME_22="/home/joris/nemaNAS/steen176/Annotation/G_ros22/braker_results2/res/augustus.hints.aa"
GFF_22="/home/joris/nemaNAS/steen176/Annotation/G_ros22/braker_results2/res/augustus.hints.gff3"

GENOME_19="/home/joris/nemaNAS/steen176/Annotation/G_ros19/G_rostochiensis_19_v0.8.fasta"
PROTEOME_19="/home/joris/nemaNAS/steen176/Annotation/G_ros19/braker_results/augustus.hints.aa"
GFF_19="/home/joris/nemaNAS/steen176/Annotation/G_ros19/braker_results/augustus.hints.gff3"

GENOME_ref   = "/home/joris/nemaNAS/steen176/reference_genome/globodera_rostochiensis.PRJEB13504.WBPS14.genomic_softmasked.fa"
PROTEOME_ref = "/home/joris/nemaNAS/steen176/reference_genome/globodera_rostochiensis.PRJEB13504.WBPS14.protein.fa"
GFF_ref      = "/home/joris/nemaNAS/steen176/reference_genome/globodera_rostochiensis.PRJEB13504.WBPS14.annotations.gff3"

if argv[1] == '19':
	PROTEOME = PROTEOME_19
	GENOME   = GENOME_19
	GFF      = GFF_19
elif argv[1] =='22':
	PROTEOME = PROTEOME_22
	GENOME   = GENOME_22
	GFF      = GFF_22
else:
    PROTEOME = PROTEOME_ref
    GENOME   = GENOME_ref
    GFF      = GFF_ref


TIDs = argv[2:]


# Dit is een class om even simpel de positie van het transcript op het genoom in op te slaan
class mRNA:
	def __init__(self, chr, start,end, strand):
		self.chr = chr
		self.start = int(start)
		self.end = int(end)
		self.strand = strand

	def __str__(self):
		return f"{self.chr}:{self.start}-{self.end}"

	def __repr__(self):
		return self.__str__()

	# Om de promotor toe te voegen extend ik de start en end positie beide met 500 (dit werkt dus niet altijd goed)
	#en selecteer ik ergens anders de promotor zelf.
	def extend_promotor(self):
		
			self.start -= 500
			if self.start < 0:
				self.start = 0

			self.end += 500


def get_fasta_map(file):
	return {record.id: str(record.seq) for record in SeqIO.parse(file, 'fasta')} # dictionary met transcript id als key en sequentie als value

def get_gff_map(gff_file):
	gff_map = {}
	with open(gff_file) as gff:
		for line in gff:
			if line.startswith("#"):
				continue
			line = line.strip().split()

			if line[2] != 'mRNA':
				continue 
			tid = line[8].split(';')[0].replace('ID=', "").replace("transcript:","")

			gff_map[tid] = mRNA(chr = line[0], start = line[3], 
								end = line[4], strand = line[6])
	return gff_map

def run_phobius(prot_seq):
	prot_seq = prot_seq.replace("*","")
	with open('/dev/shm/seq.fasta','w') as f: #/dev/shm is alleen op linux, voor windows kun je een andere temporary location kiezen
		f.write(f">test\n{prot_seq}\n")#Schrijf de sequentie van het transcript naar een fasta file

	# Command zoals je die in de terminal zou uitvoeren (als je het handmatig zou doen)
	cmd = "/home/joris/tools/phobius/phobius.pl -short /dev/shm/seq.fasta 2> /dev/null" 

	# Popen is een functie uit subprocess (Process open) waarmee je commando's vannuit python op de command line kan uitvoeren.
	p = Popen(cmd, shell = True, stdout = PIPE) 

	# Hiermee haal je de output van phobius (die het programma normaal in de terminal zou printen ) terug naar python
	out, err = p.communicate()
	out = out.decode().split()
	return out

def get_dna(tid, gff_map):
	prom_region = gff_map[tid] # wat je hier uit gff_map haalt is een instance van de mRNA class hierboven
	prom_region.extend_promotor()
	
	# Samtools is een veel gebruikt programma om met sequence data te werken, 
	# je kan er ook regios uit fasta files mee trekken, wat hier weer handig is.
	p = Popen(f"samtools faidx {GENOME} {prom_region} ", shell = True, stdout = PIPE)
	out, err = p.communicate()

	return(out.decode())

def rev_comp(seq): #Nodig voor als het gen op de reverse strand ligt (rev_comp -> reverse complement)
	comp_map = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N':'N'}
	return "".join([comp_map[nuc] for nuc in seq.upper()][::-1])

def extract_promotor(seq, strand):
	if strand == '+':
		return seq[0:501]
	else:
		return rev_comp(seq)[0:501]

def has_sigpep(prot_seq):
	out = run_phobius(prot_seq)
	if out[7] == '0':
		return False
	else:
		return True

def has_tm(prot_seq):
	out = run_phobius(prot_seq)
	if out[6] == '0':
		return False
	else:
		return True
		
def has_dog_box(tid, gff_map, MOTIF = 'ATGCCA'):
	dna_seq_extended = "".join(get_dna(tid, gff_map).split("\n")[1:])
	promotor_seq = extract_promotor(dna_seq_extended, gff_map[tid].strand)
	
	
	if MOTIF in promotor_seq: # Ik tel nu niet hoeveel/hoevaak er gevonden worden, dat zou eventueel nog kunnen
		return True
	else:
		return False


if __name__ == '__main__':
	yes = 0
	p_yes = 0
	no  = 0
	prot_map = get_fasta_map(PROTEOME)
	gff_map = get_gff_map(GFF)



	for transcript in TIDs:
		prot = prot_map[transcript]
		
		sp = has_sigpep(prot)
		tm = has_tm(prot)

		dog_box = has_dog_box(transcript, gff_map)

		line = f"{transcript}\t{sp}\t{tm}\t{dog_box}"

		if sp and dog_box and not tm:
			yes += 1
			print("**" + line)
		elif sp and not tm:
			p_yes += 1
			print("*" + line)
		else:
			no +=1
			print(" " + line)

	print(f"Total of {(yes+no+p_yes)} with {yes} full-effectors and {p_yes} partially effectors")
