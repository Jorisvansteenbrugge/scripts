#!/usr/bin/env python3
import argparse
import subprocess

class mRNA:
    def __init__(self, chrom, start, stop, name):
        self.chrom = chrom
        self.start = start
        self.stop = stop
        self.name = name

    def __str__(self):
        return f"{self.chrom}\t{self.start}\t{self.stop}\t{self.name}"

    def to_list(self):
        return self.chrom, self.start, self.stop, self.name

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_argument("--vcf", help = "Variants in vcf format (uncompressed)", dest = 'vcf', required = True)
    p.add_argument("--gff", help = "Gff file with gene regions", dest = 'gff', required = True)
    p.add_argument("--orthogroups", help = 'tsv file with descriptions of the orthogroups',
                   dest = 'orthogroups', required = True)
    p.add_argument('-c', help = 'index (0 based) of the species column in the orthogroups file',
                   dest = 'species_id', required = True, type = int)
    p.add_argument('-g', help = 'Orthogroup ID', dest = 'group_id', required = True)

    return p.parse_args()

def gff_to_dict(gff):
    d = {}
    with open(gff) as in_gff:
        for line in in_gff:
            line = line.strip().split()

            if line[2] != 'mRNA':
                continue

            tid = "".join([x for x in line[8].split(';') if 'ID=' in x]).replace('ID=','')

            d[tid] = mRNA(chrom = line[0],
                          start = line[3],
                          stop = line[4],
                          name = tid)
    return d

def get_orthogroup_ids(orthogroups, group_id, species_id):
    with open(orthogroups) as o_groups:
        header = o_groups.readline().strip().split('\t')
        print(f"User gave {header[species_id]} as species")
        for line in o_groups:
            line = line.strip().split('\t')
            if line[0] != group_id:
                continue

            return line[species_id].replace(' ','').split(',')

def write_tmp_bed(transcript_mrnas):
    with open('/dev/shm/bed.bed', 'w') as bed_file:
        for rna in transcript_mrnas:
            bed_file.write(str(rna) + '\n')

def get_vcf_regions(vcf, bedfile = '/dev/shm/bed.bed'):
    bed = f'bedtools intersect -a {bedfile} -b {vcf} -wb'
    p = subprocess.Popen(bed, shell = True, stdout = subprocess.PIPE)

    out, err = p.communicate()
    return out.decode().split('\n')


def get_orthogroup_regions(gff, orthogroups, group_id, species_id):
    gff_dict = gff_to_dict(gff)
    transcript_ids = get_orthogroup_ids(orthogroups,
                                        group_id,
                                        int(species_id))

    print(transcript_ids)
    transcript_mrnas = [gff_dict[tid] for tid in transcript_ids]

    return [transcript.to_list() for transcript in transcript_mrnas]

    #write_tmp_bed(transcript_mrnas)
   # print(get_vcf_regions(options.vcf))

# if __name__ == "__main__":
#     options = get_arguments()
#     get_orthogroup_regions(options.gff, options.orthogroups, options.group_id, options.species_id)