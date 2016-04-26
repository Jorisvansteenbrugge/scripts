library(reshape2)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
rawdata = read.table(args[1], header = TRUE, fill=TRUE)
data = melt(rawdata)
ggplot(data, aes(x= variable, y=value))+ geom_boxplot()+ xlab("Annotation files") + ylab("2LOG RPKM for each gene") +scale_y_continuous(breaks = round(seq(0, 40, by= 2),1))

ggsave(filename = args[2], dpi = 1200)
