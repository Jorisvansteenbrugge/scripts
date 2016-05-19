args <- commandArgs(trailingOnly = TRUE)


file = read.table("/run/user/1000/gvfs/sftp:host=mb07.science.ru.nl/home/jsteenbrugge/calculations/xtFullRun/aed/pitavsxenbaseMRNA.tsv",sep = "\t",header=TRUE)
col1 <- as.vector(file[,1])
col2 <- as.vector(file[,2])
result = wilcox.test(col1,col2, alternative = "two.sided")
result$p.value
print(mean(col1,na.rm = TRUE))
print(mean(col2,na.rm=TRUE))
