#!/usr/bin/Rscript

library(ggplot2)
library(gridExtra)
library(data.table)


cbbPalette <- c("steelblue", "steelblue3", "steelblue2", "steelblue1","steelblue","steelblue3","steelblue2")
scaling <- c(10,20,30,40,50,60,70,80,90,100)

args <- commandArgs(trailingOnly = TRUE)



df= read.table(args[1], header = TRUE, fill = TRUE)
x <- "Annotations"
y <- "% of peaks with gene start"

as.data.table(df) -> df
df[,percentage:=count/total*100]
as.data.frame(df) -> df
df <- df[with(df,order(df$count)), ]

ggplot(data=df, aes(annotation, percentage, fill=annotation)) +
  geom_bar(stat="identity")+
  theme_classic() +
  ggtitle("percentage of peaks matching with at least 1 gene start")+
  scale_y_continuous(limits = c(0,100), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y) +
  theme(axis.text.x = element_text(angle = 50, hjust = 1))


ggsave(args[2])


