library(ggplot2)
library(gridExtra)
library(data.table)


cbbPalette <- c("steelblue", "steelblue3", "steelblue2", "steelblue1","steelblue","steelblue3","steelblue2")
scaling <- c(10,20,30,40,50,60,70,80,90,100)
df= read.table("/home/joris/data/newBoxplotdata.tsv", header = TRUE, fill = TRUE)
x <- ""
y <- "No. of genes w/ peaks"
order = c("st6","st8", "st9","st9_2","st10.5","st11_ni","st11","st11a","st12","st16","st30")
order2 = c("Pita","xtropMRNA","Stringtie","ASM_ALT","Xenbase","xtropEST","cdna_all")
df$st <- factor(df$st, levels=order)
df$annotation <- factor(df$annotation, levels=order2)

as.data.table(df) -> df
df[,percentage:=count/total*100]
as.data.frame(df) -> df

ggplot(data=df, aes(annotation, percentage, fill=annotation)) +
  geom_bar(stat="identity")+
  ggtitle("Stage")+
  scale_y_continuous(limits = c(0,100), expand = c(0,0),breaks = scaling)+
  guides(fill=FALSE)+
  labs(x=x, y=y) +
  theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  facet_wrap(~st)




