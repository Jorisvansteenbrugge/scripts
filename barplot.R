library(ggplot2)
library(gridExtra)
cbbPalette <- c("steelblue", "steelblue3", "steelblue2", "steelblue1","steelblue","steelblue3","steelblue2")
df= read.table("/home/joris/data/pitaPeaksNo1exon_v2.tsv", header = TRUE, fill = TRUE)
 

pita <- df[df == "Pita",]
one <- ggplot(data=df, aes(stage, count)) +
  geom_bar(stat="identity")

total <- ggplot(data=df, aes(x=annotation,y=count,fill=annotation)) +
  geom_bar(stat="identity") + 
  scale_fill_manual(values= cbbPalette)+ 
  #scale_y_continuous(breaks = c(0,5,10,15,20,25,30))+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  ggtitle("Pita Chr02 10% (No. of Genes with H3K4me3 start) no 1 exon genes")+
  labs(x="Annotation", y="No. of H3K4me3 genes")


grid.arrange(total, ncol=1)



barp <- function(df){
  plt <- ggplot(df, aes(stage,count))+
    
}
