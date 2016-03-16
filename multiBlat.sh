for i in ${1}*
do
	echo $i
	blat -t=dnax -q=prot ~/data/aQueenslandica/genome/Amphimedon_queenslandica.Aqu1.30.dna_sm.genome.2bit $i blat/$(basename $i .fa).psl &
done
