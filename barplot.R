library(ggplot2)
library(gridExtra)
cbbPalette <- c("steelblue", "steelblue3", "steelblue2", "steelblue1","steelblue","steelblue3","steelblue2")
scaling <- c(0,10,20,30,40,50,60, 70)
df= read.table("/home/joris/data/pitaPeaksNo1exon_v2.tsv", header = TRUE, fill = TRUE)
x <- "Development Stage"
y <- "No. of genes w/ peaks"
order = c("stage6","stage8", "stage9","stage9_2","stage10.5","st11_ni","stage11","stage11a","stage12","stage16","stage30")
df$stage <- factor(df$stage, levels = order)

pita <- df[df == "Pita",]
pitaPlot <- ggplot(data=pita, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("Pita Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

cdna <- df[df == "cDNA_All",]
cdnaPlot <- ggplot(data=cdna, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("cDNA_All Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

xenbase <- df[df == "Xenbase",]
xenbasePlot <- ggplot(data=xenbase, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("Xenbase Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

laeEST <- df[df == "xlaevisEST",]
laeESTPlot <- ggplot(data=laeEST, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("xlaevisEST Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

laeMRNA <- df[df == "xlaevisMRNA",]
laeMRNAPlot <- ggplot(data=laeMRNA, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("xlaevisMRNA Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

tropEST <- df[df == "xtropEST",]
tropESTPlot <- ggplot(data=tropEST, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("xtropEST Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)

tropMRNA <- df[df == "xtropMRNA",]
tropMRNAPlot <- ggplot(data=tropMRNA, aes(stage, count, fill=stage)) +
  geom_bar(stat="identity")+
  ggtitle("xtropMRNA Annotation")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  scale_y_continuous(limits = c(0,70), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y)


total <- ggplot(data=df, aes(x=annotation,y=count,fill=annotation)) +
  geom_bar(stat="identity") + 
  scale_fill_manual(values= cbbPalette)+ 
  #scale_y_continuous(breaks = c(0,5,10,15,20,25,30))+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  ggtitle("Pita Chr02 10% (No. of Genes with H3K4me3 start) no 1 exon genes")+
  labs(x="Annotation", y="No. of H3K4me3 genes")+
  guides(fill=FALSE)+
  labs(x=x, y=y)



grid.arrange(cdnaPlot,pitaPlot, xenbasePlot, laeESTPlot, laeMRNAPlot, tropESTPlot, tropMRNAPlot, total, ncol=2)



