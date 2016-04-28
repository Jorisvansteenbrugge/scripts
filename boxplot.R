library(ggplot2)
df.old = read.table("/home/joris/data/boxPlotData.tsv", header = TRUE, fill = TRUE)
df = df.old
df$RPKM.log2 = log(df$RPKM.log2,2)

df = df[is.finite(df$RPKM.log2),]
order = c("xtropEST","xlaevisEST", "xtropMRNA","xlaevisMRNA","xtropCDNA_all","Xenbase","Pita")
df$Name <- factor(df$Name, levels = order)

ggplot(data=df,aes(Name,RPKM.log2, fill=Name)) + geom_boxplot(notch=TRUE) +ggtitle("Pita Chr02 10% (RPKM per annotation)")+
  scale_y_continuous(breaks = c(0,2,4,6,8,10,12,14,16,18,20,22,24,26)) +
  labs(x="Annotation", y="RPKM Log2")



