#!/usr/bin/Rscript
library(ggplot2)
library(gridExtra)
library(data.table)

#aesthetics
scaling <- c(10,20,30,40,50,60,70,80,90,100)
x <- "Annotations"
y <- "% of peaks where a gene starts"



args <- commandArgs(trailingOnly = TRUE)
df= read.table(args[1], header = TRUE, fill = TRUE)


as.data.table(df) -> df
df[,percentage:=count/total*100]
df2 <- df[order(df$percentage),]
df2$annotation <- as.character(df2$annotation)
df2$annotation <- factor(df2$annotation, levels=unique(df2$annotation))
as.data.frame(df) -> df
df <- df[with(df,order(df$count)), ]

ggplot(data=df2, aes(df2$annotation, df2$percentage)) +
  geom_bar(stat="identity", fill="steelblue")+
  theme_classic() +
  ggtitle("percentage of peaks matching with at least 1 gene start")+
  scale_y_continuous(limits = c(0,100), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y) +
  theme(axis.text.x = element_text(angle = 50, hjust = 1))

ggsave(args[2])


