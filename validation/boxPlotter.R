library(reshape2)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
xx = read.table(args[1], header = TRUE, fill=TRUE)
test = melt(xx)
plot = ggplot(test, aes(x= variable, y=value))+ geom_boxplot()+scale_y_log10()

ggsave(filename = args[2])
