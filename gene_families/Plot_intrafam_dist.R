

################################
library(tidyverse)
library(magrittr)
library(ggplot2)
library(reshape2)

Add_family_col <- function(data, fam.name){
    family <- rep(fam.name, nrow(data))
    
    return(cbind(data, family))
}

Add_family_group <- function(data, group.name){
    group <- rep(group.name, nrow(data))
    
    return(cbind(data, group))
}
    
Add_pop_col <- function(data, pop.name){
  Pop <- rep(pop.name, nrow(data))
  return(cbind(data, Pop))
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

Plot_figure <- function(data){
  ggplot(data, aes(x = centers, y = c(0), color = family)) +
    geom_point() +
    facet_wrap(~chrom) +
    theme_bw() + theme(axis.title.y=element_blank(),
                       axis.text.y = element_blank(),
                       axis.ticks.y=element_blank())
  
}

Import_table <- function(loaded_data, file, fam_name, group_name, Pop){

    data <- read.table(file)
    colnames(data) <- c("chrom","start","end","transcript","score",'strand')
    
    data %<>% Add_family_col(fam.name = fam_name)
    data %<>% Add_family_group(group.name = group_name)
    data %<>% Add_pop_col(pop.name = Pop)
    data %<>% Get_center_pos_col()
    
    
    if(is.null(loaded_data)){
      return(data) 
    } else {
      return(rbind(loaded_data, data))
    }
    
    }


Get_Number_clustered <- function(data, cluster_threshold = 4){
  clustered_chrom.names <- data$chrom %>% table %>% `>=` (cluster_threshold) %>% which %>% names
  
  clustered_gene.number <- data[which(data$chrom %in% clustered_chrom.names),] %>% nrow
  unclusered_gene.number <- nrow(data) - clustered_gene.number
  
  return(c("clustered_gene.number" =clustered_gene.number, "unclusered_gene.number"=unclusered_gene.number))
}

#####################################
data_GH5_19 <- NULL
data_GH5_19 <- Import_table(data_GH5_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH5_gr19.tsv',
                                'GH5', "CWDE", "L19")
data_GH5_22 <- NULL
data_GH5_22 <- Import_table(data_GH5_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH5_gr22.tsv',
                            'GH5', "CWDE", "L22")

data_GH30_19 <- NULL
data_GH30_19 <- Import_table(data_GH30_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH30_gr19.tsv',
                            'GH30', "CWDE", "L19")
data_GH30_22 <- NULL
data_GH30_22 <- Import_table(data_GH30_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GH30_gr22.tsv',
                            'GH30', "CWDE", "L22")

data_GS_19 <- NULL
data_GS_19 <- Import_table(data_GS_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/Gluthathione_synt_gr19.tsv',
                             'GS', "FsF", "L19")
data_GS_22 <- NULL
data_GS_22 <- Import_table(data_GS_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/Gluthathione_synt_gr22.tsv',
                             'GS', "FsF", "L22")

data_CLE_19 <- NULL
data_CLE_19 <- Import_table(data_CLE_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/CLE_gr19.tsv',
                           'CLE', "FsF", "L19")
data_CLE_22 <- NULL
data_CLE_22 <- Import_table(data_CLE_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/CLE_gr22.tsv',
                           'CLE', "FsF", "L22")

data_sprysec_19 <- NULL
data_sprysec_19 <- Import_table(data_sprysec_19, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/SPRYSEC_gr19.tsv',
                     'SPRYSEC', "Immune supression", "L19")
data_sprysec_22 <- NULL
data_sprysec_22 <- Import_table(data_sprysec_22, '~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/SPRYSEC_gr22.tsv',
                                'SPRYSEC', "Immune supression", "L22")

data_1106_22 <- NULL
data_1106_22 <- Import_table(data_1106_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr22.tsv",
                    '1106', 'Immune supression', "L22")

data_1106_19 <- NULL
data_1106_19 <- Import_table(data_1106_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/1106_gr19.tsv",
                             '1106', 'Immune supression', "L19")


data_GLAND6_22 <- NULL
data_GLAND6_22 <- Import_table(data_GLAND6_22, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr22.tsv",
                    'GLAND6', 'GLAND6', "L22")
data_GLAND6_19 <- NULL
data_GLAND6_19 <- Import_table(data_GLAND6_19, "~/nemaNAS/steen176/genome_comparisons/distances_figure/intrafamily_distance/GLAND6_gr19.tsv",
                               'GLAND6', 'GLAND6', "L22")


data_all22 <- sapply(list(
  "GH5"= data_GH5_22, "GH30" = data_GH30_22, "CLE" = data_CLE_22, "SPRYSEC" = data_sprysec_22,
  "1106"=data_1106_22,"GLAND6"=data_GLAND6_22),
                     Get_Number_clustered) %>% melt

data_all19 <- sapply(list(
  "GH5"= data_GH5_19, "GH30" = data_GH30_19, "CLE" = data_CLE_19, "SPRYSEC" = data_sprysec_19,
  "1106"=data_1106_19,"GLAND6"=data_GLAND6_19),
  Get_Number_clustered) %>% melt

plt.22 <- ggplot(data_all22, aes(x = Var2, y = value)) +
  geom_col(aes(fill=Var1), position = 'stack') +ggtitle("Gr22")
plt.19 <- ggplot(data_all19, aes(x = Var2, y = value)) +
  geom_col(aes(fill=Var1), position = 'stack') + ggtitle("Gr19")


gridExtra::grid.arrange(plt.19, plt.22, ncol = 1)
###########################################

Plot_figure(data_CLE_22) 




