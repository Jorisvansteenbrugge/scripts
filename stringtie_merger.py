import logging
from typing import Dict, Any, List, Union, Tuple

import pandas
import re
import subprocess as sp
from os import path, mkdir
from sys import exit
from glob import glob





def parse_counts_file(input_file, key):
    """

    :type input_file: str
    :type key: str
    :param input_file:
    :param key:
    :return: dictionary[transcript_name] = count_value
    """
    parsed_counts: Dict[str, str] = {}

    with open(input_file) as infile:
        for line in infile:
            if line.startswith("#"):
                continue

            line = line.strip().split("\t")

            # We are not going to report on individual exons so we only take the lines describing the full transcript
            if "transcript" not in line[2]:
                continue

            info = line[8].split("; ")
            count_value = re.search(r'' + key + ' \"([0-9]+\.[0-9]+)\"', line[8]).group(1)
            # count_value = [x for x in info if key in x]  # Here we extract the right collumn (e.g. cov, FPKM or TPM)
            # count_value = count_value[0].split('\"')[1]

            transcript_name = [x for x in info if "transcript_id" in x]
            transcript_name = transcript_name[0].split('\"')[1]

            parsed_counts[transcript_name] = count_value

    return parsed_counts


def get_transcript_ids(gff_file):
    """Parse out all transcript IDs from a GFF3 file
    This is done to get a unique list of all posibilities so we can synchronise the counts per sample later on

    :type gff_file: str

    """
    id_list = []
    with open(gff_file) as gff:
        for line in gff:
            if line.startswith("#"):
                continue

            line = line.strip().split("\t")
            if "transcript" not in line[2] and "mRNA" not in line[2]:
                continue

            info = line[8].split(";")
            try:
                value = [x for x in info if 'ID' in x]  # Here we extract the right collumn (e.g. cov, FPKM or TPM)
                value = value[0].split('=')[1]
            except IndexError:
                value = [x for x in info if 'transcript_id' in x]
                value = value[0].split(' ')[1].replace('"',"")
            id_list.append(value)

    return list(set(id_list))


def get_unique_species(samples):
    """

    :type samples: object
    :param samples:
    :return:
    """
    unique_species = set()
    for sample in samples:
        for organism_tuple in sample.species:
            unique_species.add(organism_tuple)

    return list(unique_species)


def sync_counts(counts, transcript_ids):
    synchronised_counts = []
    for t_id in transcript_ids:
        try:
            synchronised_counts.append(counts[t_id])
        except KeyError:
            synchronised_counts.append(0)

    return synchronised_counts


def write_counts_table(count_df, output_file, col_header):
    nrow = len(count_df[1])
    with open(output_file, "w") as outfile:
        outfile.write(col_header + "\n")
        for i in range(nrow):
            row = []
            for sublist in count_df:
                row.append(sublist[i])
            outfile.write("{}\n".format(";".join(map(str, row))))


def report_counts():
    """Parse the stringtie outputs and generate a table from it.

    :param options:
    :type samples: Sample
    """

    stringtiedir = "/home/joris/nemaNAS/steen176/SECPEP/stringtie_counts/"
    OUTDIR = "/tmp/test/"
    species = "Grost19"
    model_gff = "/home/joris/Desktop/Gr19_SECPEPs-2.gff3"

    countstat = "FPKM"
    statistic = 'FPKM'
    try:
        mkdir(OUTDIR)
    except FileExistsError:
        pass


    statistic_df: List[Union[Tuple[str, ...], List[Union[int, Any]]]] = []
    # Species is the full path to the genome fasta file
    species_name = species
    search_terms = "{outdir}/*.gtf".format(outdir=stringtiedir,
                                                       species=species_name)
    
    samples = glob(search_terms)
    # We then also need to know what the possible transcript names are (to ensure samples are compared
    # correctly downstream)
    transcript_ids = tuple(get_transcript_ids(model_gff))
    statistic_df.append(transcript_ids)
    for sample in samples:
        counts = parse_counts_file(sample, statistic)
        sync_values = sync_counts(counts, transcript_ids)
        statistic_df.append(sync_values)

    assert len(statistic_df) == len(samples) + 1, "dataframe built wrongly"

    sample_names = [path.basename(sample).split("_")[0] for sample in samples]

    col_header = "transcript_name;{}".format(";".join(sample_names))
    # Writing the statistic_df to a table
    output_file = "{outdir}/{species}_{countstat}_counts.csv".format(outdir=OUTDIR,
                                                                     species=species_name,
                                                                     countstat=statistic)
    write_counts_table(statistic_df, output_file, col_header)
report_counts()
