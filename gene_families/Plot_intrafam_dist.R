

################################
library(tidyverse)
library(magrittr)

Add_family_col <- function(data, fam.name){
    family <- rep(fam.name, nrow(data))
    
    return(cbind(data, family))
}

Add_family_group <- function(data, group.name){
    group <- rep(group.name, nrow(data))
    
    return(cbind(data, group))
}
    
Get_center_pos_col <- function(data){
    centers <- apply(data, 1, function(row){
        start    <- row['start'] %>% as.numeric
        end      <- row['end']   %>% as.numeric
        len.half <- (end - start) / 2
        
        return(start + len.half)
        
    })
    return(cbind(data, centers))
}

Import_table <- function(loaded_data, file, fam_name, group_name){

    data <- read.table(file)
    colnames(data) <- c("chrom","start","end","transcript","score",'strand')
    
    data %<>% Add_family_col(fam.name = fam_name)
    data %<>% Add_family_group(group.name = group_name)
    data %<>% Get_center_pos_col()
    
    if(is.null(loaded_data)){
      return(data) 
    } else {
      return(rbind(loaded_data, data))
    }
    
    }

data_sprysec <- NULL
data_sprysec <- Import_table(data_sprysec, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/SPRYSEC_gr19.tsv',
                     'SPRYSEC', "Immune supression")

data_1106_22 <- NULL
data_1106_22 <- Import_table(data_1106_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr22.tsv",
                    '1106', 'Immune supression')
data_1106_19 <- NULL
data_1106_19 <- Import_table(data_1106_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr19.tsv",
                             '1106', 'Immune supression')


data_GLAND6_22 <- NULL
data_GLAND6_22 <- Import_table(data_GLAND6_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr22.tsv",
                    'GLAND6', 'GLAND6')
data_GLAND6_19 <- NULL
 
data_GLAND6_19 <- Import_table(data_GLAND6_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr19.tsv",
                               'GLAND6', 'GLAND6')

data_GLAND5 <- NULL
data_GLAND5 <- Import_table(data_GLAND5, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND5_gr22.tsv",
                    'GLAND5', 'GLAND5')


data_FsF <- NULL
data_FsF <- Import_table(data_FsF, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/CLE_gr19.tsv',
                     'CLE_like', "Feeding site formation")
data_FsF <- Import_table(data_FsF, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/Gluthathione_synt_gr19.tsv',
                     'Gluthathione Synthetase', "Feeding site formation")

data_Cellwall <- NULL
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH5_gr19.tsv',
                     'GH5', "Cell wall degradation")
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH30_gr19.tsv',
                     'GH30', "Cell wall degradation")
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/PL3_gr19.tsv',
                     'PL3', "Cell wall degradation")
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH43_gr19.tsv',
                     'GH43', "Cell wall degradation")
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH53_gr19.tsv',
                     'GH53', "Cell wall degradation")
data_Cellwall <- Import_table(data_Cellwall, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/AG_gr19.tsv',
                     'AG', "Cell wall degradation")



ggplot(data_FsF, aes(x = centers, y = c(0), color = family)) + 
    geom_point() + 
    facet_wrap(~chrom) + 
    theme_bw() 

ggplot(data_sprysec, aes(x = centers, y = c(0), color = group)) + 
    geom_point() + 
    facet_wrap(~chrom) + 
    theme_bw() 

ggplot(data_Cellwall, aes(x = centers, y = c(0), color = family)) + 
    geom_point() + 
    facet_wrap(~chrom) + 
    theme_bw() 

ggplot(data_1106_22, aes(x = centers, y = c(0), color = family)) +
    geom_point() +
    facet_wrap(~chrom) +
    theme_bw()

ggplot(data_1106_19, aes(x = centers, y = c(0), color = family)) +
  geom_point() +
  facet_wrap(~chrom) +
  theme_bw() + theme(axis.title.y=element_blank(),
                     axis.text.y = element_blank(),
                     axis.ticks.y=element_blank())



ggplot(data_GLAND6_19, aes(x = centers, y = c(0), color = family)) +
    geom_point() +
    facet_wrap(~chrom) +
    theme_bw() + theme(axis.title.y=element_blank(),
                       axis.text.y = element_blank(),
                       axis.ticks.y=element_blank())


ggplot(data_GLAND6_22, aes(x = centers, y = c(0), color = family)) +
  geom_point() +
  facet_wrap(~chrom) +
  theme_bw()

ggplot(data_GLAND5, aes(x = centers, y = c(0), color = family)) +
    geom_point() +
    facet_wrap(~chrom) +
    theme_bw()    