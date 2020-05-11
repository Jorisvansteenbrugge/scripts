
get_number <- function(num){
    return((num))
}
read_chrom_sizes <- function(chroms.u, chrom.sizes, dataset, chr_dist_scale = 1){
    current.sizes.df <- data.frame(matrix(ncol =2, nrow =0), 
                                   stringsAsFactors = F)
    
    chrom.counts <- dataset$chrom %>% table
    
    for (chrom in chroms.u){
        size <- chrom.sizes[chrom,]
        
        current.sizes.df <- rbind(current.sizes.df, c(chrom,0), 
                                  stringsAsFactors = F)
        current.sizes.df <- rbind(current.sizes.df, c(chrom,get_number(size)), 
                                  stringsAsFactors = F)
    }
    
    
    Ypos <- sapply(1:length(chroms.u), function(x){
        rep((x*chr_dist_scale), 2)
    }) %>% as.vector()
    
    amounts <- sapply(1:length(chroms.u), function(x){
        chrom <- chroms.u[x]
        count <- chrom.counts[chrom] %>% paste0('(', .,')')
        
        c(count,count)
    }) %>% as.vector()
    
    current.sizes.df <- cbind(current.sizes.df, Ypos)
    current.sizes.df <- cbind(current.sizes.df, amounts)
    
    colnames(current.sizes.df) <- c("Chrom", "Pos", "Ypos", "Amounts")
    return(current.sizes.df)
}

get_fam_box_df <- function(){
    test.df <- data.frame(matrix(nrow = 0, ncol = 5), stringsAsFactors = F)
    #                               Family, minY, maxY, minX, maxX
    test.df <- rbind(test.df, c("GH5", 9.5, 10.5, 1000, 50000),
                     stringsAsFactors = F)
    colnames(test.df) <- c("Family", "minY", "maxY", "minX", "maxX")
    
    test.df$minY %<>% as.numeric()
    test.df$maxY %<>% as.numeric()
    test.df$minX %<>% as.numeric()
    test.df$maxX %<>% as.numeric()
    
    return(test.df)
}

get_fam_point_df <- function(dataset, sizes.df, ypos_add = 0){
    
    fam.df <- data.frame(matrix(nrow = 0, ncol = 3), stringsAsFactors = F)
    for(row.idx in 1:nrow(dataset)){
        row.c <- dataset[row.idx,]
        posX <- row.c['centers'] %>% as.numeric %>% get_number()
        chr.c <- row.c['chrom']%>% as.character
        fam <- row.c['family'] %>% as.character
        posY <- (sizes.df[which(sizes.df$Chrom == chr.c), 'Ypos'] + ypos_add)
        if(length(posY)>1){
            posY <- posY[1]
        }
        
        fam.df <- rbind(fam.df, c(fam, posY, posX), stringsAsFactors = FALSE)
    }
    
   
    colnames(fam.df) <- c("Family", "posY", "posX")
    fam.df$posY %<>% as.numeric()
    fam.df$posX %<>% as.numeric()
    
    return(fam.df)
}

Plot_family_overview <- function(dataset, chrom.sizes, title = "Title"){
    chroms.u <- dataset$chrom %>% unique
    
    sizes.df <- read_chrom_sizes(chroms.u, chrom.sizes, dataset = dataset )
    sizes.df$Pos %<>% as.numeric
    
    fam.df <- get_fam_point_df(dataset, sizes.df)
    
    
    amounts_right_shift <- 100000
    
    ggplot(sizes.df) +
        geom_line(aes(x = Pos, y = Ypos, group = Chrom)) +
      
        geom_text(aes(y = Ypos, x = c(-1*get_number(1200000)), 
                      label = Chrom), size = 7, hjust=0)  +
      
        geom_text(aes(y = Ypos, x = c(max(Pos)+amounts_right_shift),
                      label = Amounts), size = 4) +
        scale_x_continuous(limits = c(-1*get_number(1200000), 
                                      max(sizes.df$Pos)+amounts_right_shift),
                           breaks = round(seq(min(sizes.df$Pos), max(sizes.df$Pos), by = 1000000))) +
        geom_point(data = fam.df, aes(x=posX, y = posY, fill = Family, 
                                      color = 'black'), 
                   shape = 25, color = 'black', size = 4) + 
        ggtitle(title) +
        theme_classic() +
        xlab("Scaffold Position")+
        theme(plot.title = element_text(size = 30),
              axis.title.y = element_blank(),
              axis.text.y=element_blank(),
              axis.ticks.y=element_blank(),
              axis.text.x = element_text(size = 20),
              axis.title.x = element_text(size = 20)) 
    
    
    
        
    
  
}
