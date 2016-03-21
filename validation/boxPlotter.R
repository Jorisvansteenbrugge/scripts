library(reshape2)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
rawdata = read.table(args[1], header = TRUE, fill=TRUE)
data = melt(rawdata)
plot = ggplot(data, aes(x= variable, y=value))+ geom_boxplot()+scale_y_log10()

ggsave(filename = args[2], dpi = 1200, scale = 2)
