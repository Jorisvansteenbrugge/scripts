#!/usr/bin/env python3
from sys import argv, exit, version
from Bio import SeqIO
from os import path
from difflib import SequenceMatcher as SM

bact_fwd = ["GTGCCAGCAGCCGCGGTA", "GTGCCAGCCGCCGCGGTA"]

bact_rev = ["GGACTACAAGGGTATCTAAT", "GGACTACCAGGGTATCTAAT",
            "GGACTACTAGGGTATCTAAT", "GGACTACACGGGTATCTAAT",
            "GGACTACCCGGGTATCTAAT", "GGACTACTCGGGTATCTAAT",
            "GGACTACAGGGGTATCTAAT", "GGACTACCGGGGTATCTAAT",
            "GGACTACTGGGGTATCTAAT", "GGACTACAAGGGTTTCTAAT",
            "GGACTACCAGGGTTTCTAAT", "GGACTACTAGGGTTTCTAAT",
            "GGACTACACGGGTTTCTAAT", "GGACTACCCGGGTTTCTAAT",
            "GGACTACTCGGGTTTCTAAT", "GGACTACAGGGGTTTCTAAT",
            "GGACTACCGGGGTTTCTAAT", "GGACTACTGGGGTTTCTAAT"]

fungi_fwd = ["CGATAACGAACGAGACCT", "CGTTAACGAACGAGACCT"]
fungi_rev = ["AACCATTCAATCGGTAAT", "AACCATTCAATCGGTACT",
             "AACCATTCAATCGGTAGT", "AACCATTCAATCGGTATT",
             "ACCCATTCAATCGGTAAT", "ACCCATTCAATCGGTACT",
             "ACCCATTCAATCGGTAGT", "ACCCATTCAATCGGTATT",
             "AGCCATTCAATCGGTAAT", "AGCCATTCAATCGGTACT",
             "AGCCATTCAATCGGTAGT", "AGCCATTCAATCGGTATT",
             "ATCCATTCAATCGGTAAT", "ATCCATTCAATCGGTACT",
             "ATCCATTCAATCGGTAGT", "ATCCATTCAATCGGTATT"]

protozoa_fwd = ["GTACACACCGCCCGTC"]
protozoa_rev = ["TGATCCTTCTGCAGGTTCACCTAC"]

metazoa_fwd = ["AGAGGTGAAATTCTTGGACCGC", "AGAGGTGAAATTCTTGGACCGT",
               "AGAGGTGAAATTCTTGGATCGC", "AGAGGTGAAATTCTTGGATCGT"]
metazoa_rev = ["ACATCTAAGGGCATCACAGAC"]

fupro_fwd = ["GCCAGCAACCGCGGTAAC", "GCCAGCAACCGCGGTAAT",
             "GCCAGCAACTGCGGTAAT", "GCCAGCAACTGCGGTAAC",
             "GCCAGCACCCGCGGTAAC", "GCCAGCACCCGCGGTAAT",
             "GCCAGCACCTGCGGTAAT", "GCCAGCACCTGCGGTAAC",
             "GCCAGCAGCCGCGGTAAC", "GCCAGCAGCCGCGGTAAT",
             "GCCAGCAGCTGCGGTAAT", "GCCAGCAGCTGCGGTAAC"]
fupro_rev = ["CCGTCAATTACTTCAAAT", "CCGTCAATTACTTTAAGT",
             "CCGTCAATTACTTCAAGT", "CCGTCAATTACTTTAAAT",
             "CCGTCAATTCCTTCAAAT", "CCGTCAATTCCTTTAAGT",
             "CCGTCAATTCCTTCAAGT", "CCGTCAATTCCTTTAAAT",
             "CCGTCAATTTCTTCAAAT", "CCGTCAATTTCTTTAAGT",
             "CCGTCAATTTCTTCAAGT", "CCGTCAATTTCTTTAAAT"]

universal_fwd = ["GTGCCAGCAGCCGCGGTAA", "GTGCCAGCCGCCGCGGTAA",
                 "GTGTCAGCAGCCGCGGTAA", "GTGTCAGCCGCCGCGGTAA"]
universal_rev = ["CCGCCAATTCATTTGAGTT", "CCGTCAATTCATTTGAGTT",
                 "CCGCCAATTTATTTGAGTT", "CCGTCAATTTATTTGAGTT",
                 "CCGCCAATTCCTTTGAGTT", "CCGTCAATTCCTTTGAGTT",
                 "CCGCCAATTTCTTTGAGTT", "CCGTCAATTTCTTTGAGTT",
                 "CCGCCAATTCATTTAAGTT", "CCGTCAATTCATTTAAGTT",
                 "CCGCCAATTTATTTAAGTT", "CCGTCAATTTATTTAAGTT",
                 "CCGCCAATTCCTTTAAGTT", "CCGTCAATTCCTTTAAGTT",
                 "CCGCCAATTTCTTTAAGTT", "CCGTCAATTTCTTTAAGTT"]

bacteria_primers = (bact_fwd, bact_rev)
fungi_primers = (fungi_fwd, fungi_rev)
protozoa_primers = (protozoa_fwd, protozoa_rev)
metazoa_primers = (metazoa_fwd, metazoa_rev)
fupro_primers = (fupro_fwd, fupro_rev)
universal_primers = (universal_fwd, universal_rev)


def test_primer_set(read_str, primers):
    for fwd_primer in primers[0]:
        read_fwd_part = read_str[0:len(fwd_primer)]

        match_ratio = SM(None, read_fwd_part, fwd_primer).ratio()

        if match_ratio >= 0.9:
            return True

    return False


def get_sample_base(file_name):
    return path.basename(file_name).replace('.fastq', '')


# for fwd_reads in *_R1_ *
#    do
#    python split_taxa_mod_UseqSC.py $fwd_reads
# done


fwd_file = argv[1]
rev_file = argv[1].replace("_R1_", "_R2_")


fwd_fastq = list(SeqIO.parse(fwd_file, 'fastq'))
rev_fastq = list(SeqIO.parse(rev_file, 'fastq'))

fwd_base = get_sample_base(fwd_file)
fwd_out_bact = f"./{fwd_base}_bacteria.fastq"
fwd_out_fungi = f"./{fwd_base}_fungi.fastq"
fwd_out_metazoa = f"./{fwd_base}_metazoa.fastq"
fwd_out_protozoa = f"./{fwd_base}_protozoa.fastq"
fwd_out_fupro = f"./{fwd_base}_fupro.fastq"
fwd_out_universal = f"./{fwd_base}_universal.fastq"
fwd_out_nothing = f"./{fwd_base}_nomatch.fastq"

rev_base = get_sample_base(rev_file)
rev_out_bact = f"./{rev_base}_bacteria.fastq"
rev_out_fungi = f"./{rev_base}_fungi.fastq"
rev_out_metazoa = f"./{rev_base}_metazoa.fastq"
rev_out_protozoa = f"./{rev_base}_protozoa.fastq"
rev_out_fupro = f"./{rev_base}_fupro.fastq"
rev_out_universal = f"./{rev_base}_universal.fastq"
rev_out_nothing = f"./{rev_base}_nomatch.fastq"

b_records_f = []
b_records_r = []

m_records_f = []
m_records_r = []

f_records_f = []
f_records_r = []

p_records_f = []
p_records_r = []

fp_records_f = []
fp_records_r = []

u_records_f = []
u_records_r = []

nothing_f = []
nothing_r = []

for i in range(len(fwd_fastq)):
    print(i)
    f_record = fwd_fastq[i]
    r_record = rev_fastq[i]

    f_read = str(f_record.seq)
    r_read = str(r_record.seq)

    bact_primer = test_primer_set(f_read, bacteria_primers)
    fungal_primer = test_primer_set(f_read, fungi_primers)
    metazoan_primer = test_primer_set(f_read, metazoa_primers)
    protist_primer = test_primer_set(f_read, protozoa_primers)
    fupro_primer = test_primer_set(f_read, fupro_primers)
    universal_primer = test_primer_set(f_read, universal_primers)

    # output
    if bact_primer:
        b_records_f.append(f_record)
        b_records_r.append(r_record)
    elif metazoan_primer:
        m_records_f.append(f_record)
        m_records_r.append(r_record)

    elif protist_primer:
        p_records_f.append(f_record)
        p_records_r.append(r_record)

    elif fungal_primer:
        f_records_f.append(f_record)
        f_records_r.append(r_record)

    elif fupro_primer:
        fp_records_f.append(f_record)
        fp_records_r.append(r_record)

    elif universal_primer:
        u_records_f.append(f_record)
        u_records_r.append(r_record)

    else:
        nothing_f.append(f_record)
        nothing_r.append(r_record)

SeqIO.write(b_records_f, fwd_out_bact, 'fastq')
SeqIO.write(b_records_r, rev_out_bact, 'fastq')

SeqIO.write(m_records_f, fwd_out_metazoa, 'fastq')
SeqIO.write(m_records_r, rev_out_metazoa, 'fastq')

SeqIO.write(f_records_f, fwd_out_fungi, 'fastq')
SeqIO.write(f_records_r, rev_out_fungi, 'fastq')

SeqIO.write(p_records_f, fwd_out_protozoa, 'fastq')
SeqIO.write(p_records_r, rev_out_protozoa, 'fastq')

SeqIO.write(fp_records_f, fwd_out_fupro, 'fastq')
SeqIO.write(fp_records_r, rev_out_fupro, 'fastq')

SeqIO.write(u_records_f, fwd_out_universal, 'fastq')
SeqIO.write(u_records_r, rev_out_universal, 'fastq')

SeqIO.write(nothing_f, fwd_out_nothing, 'fastq')
SeqIO.write(nothing_r, rev_out_nothing, 'fastq')
print(f'Nothing: {len(nothing_f)}')
