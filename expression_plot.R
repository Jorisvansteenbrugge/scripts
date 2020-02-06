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

gr19_ids <- c('g11055','g11056','g11057','g11058','g11059','g11060','g11061','g11062','g11063','g11064','g11065','g11066','g11067','g11068','g11069','g11070','g11071','g11072','g11073','g11074','g11075','g11076','g11077','g11078','g11079','g11080','g11081','g11082','g11083','g11084','g11085','g11086','g11087','g11088','g11089','g11090','g11091','g11092','g11093','g11094','g11095','g11096','g11097','g11098','g11099','g11100','g11101','g11102','g11103','g11104','g11105','g11106','g11107','g11108','g11109','g11110','g11111','g11112','g11113','g11114','g11115','g11116','g11117','g11118','g11119','g11120','g11121','g11122','g11123','g11124','g11125','g11126','g11127','g11128','g11129','g11130','g11131','g11132','g11133','g11134')
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

#J2s
plot_df.j2 <- plot_df[which(plot_df$Sample %in% c("J2_SRR1873829","J2_SRR1873820")),]
plot_df.j2.filtered <- plot_df.j2[which(plot_df.j2$TPM>=10),]

ggplot(data = plot_df) + geom_line(aes(x = Sample, y = TPM, group = TID)) +  theme(axis.text.x = element_text(angle = 90))  
ggplotly()
