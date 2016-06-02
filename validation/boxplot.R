library(ggplot2)


df <- read.table("/home/joris/data/outfiletest2.tsv", header = TRUE, fill = TRUE)



df$RPKM.log2 = log(df$RPKM.log2,2)

#df = df[is.finite(df$RPKM.log2),]
order <- c("xenbase","pita", "xlaevisMRNA13", "xtrop_mRNA", "stringtie","xlaevis_EST", "xtrop_EST")
df$Name <- factor(df$Name, levels = order)

ggplot(data=df,aes(x=Name,y=RPKM.log2, fill=Name)) + 
  geom_boxplot(notch=TRUE) +
  ggtitle("Pita Chr02 10% no 1 exon genes (RPKM per annotation)")+
  scale_y_continuous(breaks = c(0,2,4,6,8,10,12,14,16,18,20,22,24,26)) +
  labs(x="Annotation", y="RPKM Log2")+
  theme(axis.text.x = element_text(angle = 50, hjust = 1))

