Swap_names_pallida <- function(vec){
    sapply(vec, function(name){
        name <- strsplit(name, split = '_') %>% unlist %>% .[4:5] %>% paste0(collapse = '_')
    }) %>% as.character %>% return
}
D383_1106 <- NULL
D383_1106 <- Import_table(D383_1106, 
                            '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/D383/1106_Gpal_D383.bed',
                            '1106', "1106", "D383")
D383_1106$chrom %<>% Swap_names_pallida()


D383_4D06 <- NULL
D383_4D06 <- Import_table(D383_4D06, 
                          '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/D383/GLAND6_Gpal_D383.bed',
                          '4D06', "4D06", "D383")
D383_4D06$chrom %<>% Swap_names_pallida()

D383_HYP <- NULL
D383_HYP <- Import_table(D383_HYP, 
                          '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/D383/HYP_Gpal_D383.bed',
                          'HYP', "HYP", "D383")
D383_HYP$chrom %<>% Swap_names_pallida()

D383_SPRYSEC <- NULL
D383_SPRYSEC <- Import_table(D383_SPRYSEC, 
                         '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/D383/SPRYSECs_Gpal_D383.bed',
                         'SPRYSEC', "SPRYSEC", "D383")
D383_SPRYSEC$chrom %<>% Swap_names_pallida()
#############################
setwd('/home/joris/tools/scripts/gene_families/')
source('Plot_gene_families.R')
chrom.sizes.D383 = read.table("D383.sizes", row.names = 1)
rownames(chrom.sizes.D383) %<>% Swap_names_pallida


Plot_family_overview(D383_1106, chrom.sizes.D383, title = "G. pallida D383 1106")
Plot_family_overview(D383_4D06, chrom.sizes.D383, title = "G. pallida D383 4D06")
Plot_family_overview(D383_HYP, chrom.sizes.D383, title = "G. pallida D383 HYP")
Plot_family_overview(D383_SPRYSEC, chrom.sizes.D383, title = "G. pallida D383 SPRYSEC")
