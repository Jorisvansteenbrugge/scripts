#!/bin/bash
# Bash script to download a bunch of *.sra files from the NCBI SRA, using 
#apsera

max_bandwidth_mbps=50

# These SRA files are for the durum genome
files=(
  'SRR1513978.sra',
  'SRR1511621.sra',
  'SRR1511620.sra',
  'SRR1511619.sra',
  'SRR1511618.sra'
)

for file in "${files[@]}"; do
  echo "${file}"
~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh -k1 -QTr -l${max_bandwidth_mbps}m anonftp@ftp-trace.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/${file:0:3}/${file:0:6}/${file%.sra}/${file} ./
  if [[ ! -e ${file%.sra}.aspx && ! -e ${file%.sra}.fastq.gz ]]; then
    echo -n "  Extracting data into FASTQ format ... "
    fastq-dump --split-files ${file}
    echo "DONE"
  else
    echo "  Skipping"
  fi
done
