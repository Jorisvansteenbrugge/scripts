for i in ./*.bam
do
	stringtie $i -p 4 -o $(basename $i .bam).gtf
done
