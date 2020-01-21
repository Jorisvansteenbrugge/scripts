
library(reticulate)
library(PopGenome)
use_python('/home/joris/tools/miniconda3/bin/python', required = TRUE)
source_python('/home/joris/tools/scripts/regional_snp_freq.py')

vcfgz_file <- "all.variants.vcf.gz"

group_transcripts <- get_orthogroup_regions("/home/joris/nemaNAS/steen176/Annotation/G_ros19/braker_results/augustus.hints.gff3",
                                            "/home/joris/nemaNAS/steen176/genome_comparisons/Ortofinder_clades/output_orthofinder_all_genomes/Results_Jan13/Orthogroups/Orthogroups.tsv",
                                            "OG0001701", 9)
lapply(group_transcripts, function(x) return( c(x)))

Get_sample_names <- function(vcfgz){
  vcf_handle <- .Call("VCF_open", vcfgz_file)
  ind <- .Call("VCF_getSampleNames", vcf_handle)
  return(ind)
}

Plot_interpolation <- function(interpolations, window_size, scaff_name){

  plot(predict(interpolations[[1]]), type = 'l', xaxt='n', xlab = 'position (Mb)',
       ylab = 'nucleotide diversity', main = paste0(scaff_name, " (", window_size/1000, 'kb windows)'), ylim = c(0,0.01))

  for (inter_idx in 2: length(interpolations)){
    lines(predict(interpolations[[inter_idx]]))
  }



  #legend ("top", c("M", "S","X"), col = c('black', 'blue','red'), lty = c(1,1,1))
}

Interpolate_samples <- function(number_of_windows, nucdiv, span = 0.05){
  interpolations <- list()

  for (sample_idx in 1:ncol(nucdiv)){
    interpolations[[sample_idx]] <- loess(nucdiv[,sample_idx] ~ number_of_windows, span = span)
  }
  return(interpolations)
}

Scaffold_wide_diversity <- function(vcfgz, scaff_name, scaff_size, window_size = 10000){
  sample_names <-  Get_sample_names(vcfgz)
  #


  GENOME.class <- readVCF(vcfgz_file, numcols = 1000000, tid = scaff_name,
                          frompos = 1, topos = scaff_size,
                          gffpath ="/home/joris/nemaNAS/steen176/Annotation/G_ros19/braker_results/augustus.hints.gff3" )

  GENOME.class <- set.populations(GENOME.class, lapply(sample_names, print), diploid = TRUE)
  #Determine if snp synonymou sor non-synonymous
  GENOME.class <- set.synnonsyn(GENOME.class, ref.chr= "/home/joris/nemaNAS/steen176/Annotation/G_ros19/G_rostochiensis_19_v0.8.fasta")

  GENOME.class <- MKT(GENOME.class)



  # Sliding 10kb test
  GENOME.class.slide <- sliding.window.transform(GENOME.class, window_size, window_size, type = 2)
  genome.pos <- sapply(GENOME.class.slide@region.names, function(x){
    split <- strsplit(x, ' ')[[1]][c(1,3)]
    val <- mean(as.numeric(split))
    return(val)
  })

  number_of_windows <- length(GENOME.class.slide@region.names)

  GENOME.class.slide <- diversity.stats(GENOME.class.slide)
  nucdiv <- GENOME.class.slide@nuc.diversity.within
  nucdiv <- nucdiv / number_of_windows

  #Smooth lines via spline interpolation
  ids <- 1:number_of_windows
  interpolation <- Interpolate_samples(ids, nucdiv)

  Plot_interpolation(interpolations = interpolation,window_size = window_size, scaff_name = scaff_name)

}

Scaffold_wide_diversity(vcfgz_file, 'Gr19_scaffold35', 2800000, window_size = 10000)



GENOME.class <- F_ST.stats(GENOME.class)
get.F_ST(GENOME.class)
