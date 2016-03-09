for i in ${1}*
do
	echo $i
	blat -t=dnax -q=prot blat/xt9_0.2bit $i blat/$(basename $i .fa).psl &
done
