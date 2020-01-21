library(magrittr); library(ggplot2)
library(plotly)
counts <- read.csv2("~/nemaNAS/steen176/Annotation/G_ros19/Grost19_TPM_counts.csv",
                    row.names = 1, stringsAsFactors = F)

sample_list <- list(
    "SRR1873820.gtf" = "J2_SRR1873820",
    "SRR1873827.gtf" = "Hydrated_cyst_48h_SRR1873827",
    "SRR1873829.gtf" = "J2_SRR1873829",
    "SRR1873812.gtf" = "Dry_cyst_SRR1873812",
    "SRR1873815.gtf" = "Hydrated_cyst_1h_SRR1873815",
    "ERR202480.gtf" = "x_ERR202480",
    "ERR202487.gtf" = "x_ERR202487",
    "SRR1873814.gtf" = "Hydrated_cyst_15m_SRR1873814",
    "SRR1873813.gtf" = "Hydrated_cyst_SRR1873813",
    "SRR1873828.gtf" = "Hydrated_cyst_7d_SRR1873828",
    "SRR1873826.gtf" = "Hydrated_cyst_24h_SRR1873826",
    "ERR1173511.gtf" = "Female_14dpi_ERR1173511",
    "SRR1873821.gtf" = "Dry_cyst_SRR1873821",
    "ERR202481.gtf" = "Female14dpi_ERR202481",
    "SRR1873817.gtf" = "Hydrated_cyst_24h_SRR1873817",
    "SRR1873819.gtf" = "Hydrated_cyst_7d_SRR1873819",
    "ERR202479.gtf" = "x_ERR202479",
    "SRR1873822.gtf" = "Hydrated_cyst_SRR1873822",
    "SRR1873825.gtf" = "Hydrated_cyst_8h_SRR1873825",
    "ERR1173512.gtf" = "Female14dpi_ERR1173512",
    "SRR1873824.gtf" = "Hydrated_cyst_1h_SRR1873824",
    "SRR1873823.gtf" = "Hydrated_cyst_15m_SRR1873823",
    "SRR1873818.gtf" = "Hydrated_cyst_48h_SRR1873818",
    "SRR1873816.gtf" = "Hydrated_cyst_8h_SRR1873816")

colnames(counts) <- sapply(colnames(counts), function(x)return(sample_list[[x]])) %>% as.character


plot_mat <- matrix(ncol = 3, nrow = 0)



gr22_ids <- c("g6045.t1","g6065.t1","g6134.t1","g16492.t1","g9861.t1","g2809.t1","g13440.t1",
         "g18236.t1","g18237.t1","g2712.t1","g2726.t1","g2771.t1","g1514.t1","g1544.t1",
         "g1551.t1","g7259.t1","g7286.t1","g7331.t1","g11888.t1")

gr19_ids <- c('g5945.t1','g5942.t1','g9203.t1','g9202.t1','g5969.t1','g9201.t1','g9199.t1','g5964.t1','g9198.t3','g9198.t2','g9198.t1','g9200.t1','g13099.t1','g16950.t1','g13093.t1','g10093.t1','g10105.t3','g10114.t1','g10114.t2','g10114.t3','g10116.t1','g10126.t1','g10141.t1','g10274.t1','g11403.t1','g11410.t1','g11528.t1','g11543.t1','g12955.t1','g12956.t1','g12958.t1','g12958.t2','g15421.t1','g15422.t1','g16221.t1','g17089.t1','g17192.t1','g3856.t1','g452.t1','g454.t1','g468.t1','g478.t1','g482.t1','g491.t1','g503.t1','g507.t1','g523.t1','g540.t1','g6078.t1','g6105.t1','g6105.t2','g6107.t1','g6184.t1','g6188.t1','g6188.t2','g619.t1','g6193.t1','g631.t1','g634.t1','g7100.t1','g7103.t1','g7105.t1','g7269.t1','g7270.t1','g8321.t1','g8321.t3','g9187.t1','g9190.t1','g9191.t1','g9192.t1','g10115.t1','g10120.t1','g10161.t1','g10836.t1','g10836.t2','g10836.t3','g10836.t4','g12077.t1','g12084.t1','g12107.t1','g12114.t1','g12117.t1','g12122.t1','g12726.t1','g515.t1','g807.t1','g8413.t1','g9238.t1','g9238.t2')
#ids <- gr22_ids
ids <- gr19_ids

subs <- counts[ids,]

for (i in 1: nrow(subs)){
    row <- subs[i,]
    tid <- rownames(row) %>% .[1]
    for (y in 1: length(row)){
        cid <- colnames(row)[y]
        
        a <- c(as.numeric(row[y]), tid, cid)
        plot_mat <- rbind(plot_mat, a )
    }
    
}

plot_df <- as.data.frame(plot_mat, stringsAsFactors = F)
colnames(plot_df) <- c("TPM", "TID","Sample")

plot_df$TPM %<>% as.numeric

ggplot(data = plot_df) + geom_line(aes(x = Sample, y = TPM, group = TID)) +  theme(axis.text.x = element_text(angle = 90))  
ggplotly()
